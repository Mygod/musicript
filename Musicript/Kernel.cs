using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text.RegularExpressions;
using System.Windows;
using System.Xml.Linq;
using Mygod.Windows;
using Mygod.Xml.Linq;

namespace Mygod.Musicript
{
    public sealed class Instrument
    {
        private Instrument(Assembly assembly, string className)
        {
            sample = assembly.GetType("Mygod.Musicript.Instruments." + className)
                .GetMethod("Sample", BindingFlags.Public | BindingFlags.Static, null, new[] { typeof(double) }, null);
        }

        public double Sample(double time)
        {
            return (double) sample.Invoke(null, new object[] { time });
        }

        private readonly MethodInfo sample;

        private static readonly Dictionary<string, Assembly> ImportedAssemblies = new Dictionary<string, Assembly>();
        public static readonly Dictionary<string, Instrument> Instruments = new Dictionary<string, Instrument>();

        public static void Import(string path, string classNames, string dir = null)
        {
            if (string.IsNullOrWhiteSpace(classNames)) return;  // MEH I DON'T EVEN CARE
            string fullPath;
            path += ".dll";
            if (dir == null || !File.Exists(fullPath = Path.Combine(dir, "Instruments", path)))
                if (!File.Exists(fullPath = Path.Combine(CurrentApp.Directory, "Presets/Instruments", path)))
                    throw new FileNotFoundException();
            var temp = fullPath.ToLowerInvariant();
            if (!ImportedAssemblies.ContainsKey(temp)) ImportedAssemblies.Add(temp, Assembly.LoadFrom(fullPath));
            foreach (var className in classNames.Split(new[] { ',' }, StringSplitOptions.RemoveEmptyEntries))
                Instruments[className] = new Instrument(ImportedAssemblies[temp], className);
        }
    }

    public abstract class TrackNode
    {
        protected TrackNode(double value)
        {
            Value = value;
        }
        protected TrackNode(Match match) : this(match.Groups[8].Value == "-" ? double.NaN : double.Parse(match.Groups[8].Value))
        {
        }
        public double Value;

        public static TrackNode Create(Match match)
        {
            return match.Groups[2].Success ? (TrackNode) new ConfigureNode(match) : new Note(match);
        }
    }
    public sealed class Note : TrackNode
    {
        private static readonly int[] NoteMappings = { 0, 2, 4, 5, 7, 9, 11 };
        private static readonly Dictionary<string, int> SyllableMappings = new Dictionary<string, int>
        {
            { "do", 0 }, { "di", 1 }, { "re", 2 }, { "ri", 3 }, { "mi", 4 }, { "fa", 5 },
            { "fi", 6 }, { "so", 7 }, { "si", 8 }, { "la", 9 }, { "li", 10 }, { "ti", 11 }
        };

        public Note(double frequency, double length) : base(length)
        {
            Frequency = frequency;
        }
        public Note(Match match) : base(match)
        {
            if (match.Groups[1].Value == "-") Frequency = 0;
            else if (match.Groups[3].Success) Frequency = double.Parse(match.Groups[3].Value);
            else
            {
                int height;
                if (match.Groups[5].Success)
                {
                    var ch = match.Groups[5].Value[0];
                    height = NoteMappings[(ch + 7 - (ch <= '7' ? '1' : 'c')) % 7];
                    foreach (var c in match.Groups[6].Value)
                        switch (c)
                        {
                            case 'b':
                                height--;
                                break;
                            case '#':
                                height++;
                                break;
                        }
                }
                else height = SyllableMappings[match.Groups[4].Value];
                height += int.Parse(match.Groups[7].Value) * 12;
                Frequency = 8.17579891564375 * Math.Pow(2, height / 12.0);
            }
        }

        public readonly double Frequency;
        public double Length { get { return Value; } set { Value = value; } }
    }
    public sealed class ConfigureNode : TrackNode
    {
        public ConfigureNode(string type, double value) : base(value)
        {
            Type = type;
        }
        public ConfigureNode(Match match) : base(match)
        {
            Type = match.Groups[2].Value;
        }

        public readonly string Type;
    }
    public sealed class Track : List<TrackNode>
    {
        private static readonly Regex NoteMatcher = new Regex(
            @"((sd|st)|f([0-9.]+)|-|(do|di|re|ri|mi|fa|fi|so|si|la|li|ti|([a-g1-7])\s*([#b]*))\s*([+-]?\s*\d+))\s*(-|[0-9.]+)",
            RegexOptions.Compiled | RegexOptions.Singleline);
        public Track(XElement element)
        {
            currentNoteStartTime = BeginAt = element.GetAttributeValueWithDefault<TimeSpan>("BeginAt").TotalSeconds;
            Instrument = Instrument.Instruments[element.GetAttributeValue("Instrument")];
            Tempo = element.GetAttributeValueWithDefault("Tempo", 60.0);
            Dynamics = element.GetAttributeValueWithDefault("Dynamics", 1.0);
            var sum = 0.0;
            foreach (var node in from Match match in NoteMatcher.Matches(element.Value.ToLower()) select TrackNode.Create(match))
            {
                Add(node);
                var note = node as Note;
                if (note != null) sum += note.Length;
            }
            Length = 60 * sum / Tempo;
        }

        public readonly double BeginAt, Length;
        public readonly Instrument Instrument;
        public double Tempo, Dynamics;

        private int currentNodeIndex;
        private double currentNoteStartTime;

        public double Update(double time)
        {
            if (time < BeginAt || currentNodeIndex >= Count) return 0;
            var i = currentNodeIndex;
            double tempo = Tempo, t = currentNoteStartTime;
            while (i < Count)
            {
                var node = this[i];
                var note = node as Note;
                if (note != null)
                {
                    t += 60 * note.Length / tempo;
                    if (t > time) break;
                }
                else
                {
                    var cn = (ConfigureNode) node;
                    if (cn.Type == "st") tempo = cn.Value;
                }
                i++;
            }
            if (i >= Count)
            {
                currentNodeIndex = Count;
                return 0;
            }
            while (currentNodeIndex < i)
            {
                var node = this[currentNodeIndex];
                var note = node as Note;
                if (note != null) currentNoteStartTime += 60 * note.Length / tempo;
                else
                {
                    var cn = (ConfigureNode) node;
                    switch (cn.Type)
                    {
                        case "sd":
                            Dynamics = cn.Value;
                            break;
                        case "st":
                            Tempo = cn.Value;
                            break;
                    }
                }
                currentNodeIndex++;
            }
            var freq = ((Note) this[currentNodeIndex]).Frequency;
            return freq < 1e-8 ? 0 : Instrument.Sample((time - currentNoteStartTime) * freq) * Dynamics;
        }
    }
    public sealed class Channel : List<Track>
    {
        public readonly double Length;

        public Channel(XElement element)
        {
            foreach (var track in element.Elements("Track").Select(e => new Track(e)))
            {
                Add(track);
                var length = track.BeginAt + track.Length;
                if (length > Length) Length = length;
            }
        }

        internal double Update(double time)
        {
            return this.Sum(track => track.Update(time));
        }
    }
    public sealed class Project : List<Channel>
    {
        public Project(string mcpPath)
        {
            var dir = Path.GetDirectoryName(mcpPath);
            var root = XHelper.Load(mcpPath).Root;
            Name = root.GetAttributeValue("Name");
            Composer = root.GetAttributeValue("Composer");
            Editor = root.GetAttributeValue("Editor");
            Looped = root.GetAttributeValueWithDefault<bool>("Looped");
            foreach (var import in root.Elements("ImportInstrument"))
                Instrument.Import(import.GetAttributeValue("Path"), import.GetAttributeValue("Names"), dir);
            foreach (var channel in root.Elements("Channel").Select(element => new Channel(element)))
            {
                Add(channel);
                if (Length < channel.Length) Length = channel.Length;
            }
        }

        public readonly double Length;
        public readonly string Name, Composer, Editor;
        public readonly bool Looped;

        public Stream Compile(int bytesPerSample = 2, uint samplesPerSecond = 44100)
        {
            return new ProjectWavStream(this, bytesPerSample, samplesPerSecond);
        }

        internal double Update(double time)
        {
            var result = this.Sum(channel => channel.Update(time));
            return result > 1 ? 1 : result < -1 ? -1 : result;
        }
    }

    internal sealed class ProjectWavStream : Stream
    {
        internal ProjectWavStream(Project project, int bytesPerSample = 2, uint samplesPerSecond = 44100)
        {
            if ((this.bytesPerSample = bytesPerSample) < 0)
            {
                actualBytesPerSample = -bytesPerSample;
                header[20] = 3;
            }
            else actualBytesPerSample = bytesPerSample;
            if (project.Count > 65535) throw new FormatException("声道数不能超过 65535！");
            if (project.Count * actualBytesPerSample > 65535) throw new FormatException("声道数/位深度过大！");
            var frameSize = (ushort)(project.Count * actualBytesPerSample);
            if ((long)samplesPerSecond * frameSize > 4294967295) throw new FormatException("声道数/位深度/取样率过大！");
            var dataChunkSize = (long) Math.Ceiling(samplesPerSecond * project.Length) * frameSize;
            length = dataChunkSize + 36;
            if (length > 4294967295)
            {
                MessageBox.Show("声道数/位深度/取样率/音乐长度过大使得音乐长度超出了 4G！部分音乐会被截断。",
                                "警告", MessageBoxButton.OK, MessageBoxImage.Exclamation);
                dataChunkSize = 4294967259 / frameSize * frameSize;
                length = dataChunkSize + 36;
            }
            Array.Copy(BitConverter.GetBytes((uint) length), 0, header, 4, 4);
            length += 8;
            Array.Copy(BitConverter.GetBytes((ushort)((this.project = project).Count)), 0, header, 22, 2);
            Array.Copy(BitConverter.GetBytes(this.samplesPerSecond = samplesPerSecond), 0, header, 24, 4);
            Array.Copy(BitConverter.GetBytes((uint) ((long) samplesPerSecond * frameSize)), 0, header, 28, 4);
            Array.Copy(BitConverter.GetBytes(frameSize), 0, header, 32, 2);
            Array.Copy(BitConverter.GetBytes((ushort)(bytesPerSample << 3)), 0, header, 34, 2);
            Array.Copy(BitConverter.GetBytes((uint)dataChunkSize), 0, header, 40, 4);
        }

        private readonly Project project;
        private readonly int bytesPerSample, actualBytesPerSample;
        private readonly uint samplesPerSecond;
        private readonly long length;
        private uint position;
        private readonly byte[] header =
        {
            0x52, 0x49, 0x46, 0x46, 
            0, 0, 0, 0,                 // length
            0x57, 0x41, 0x56, 0x45, 0x66, 0x6D, 0x74, 0x20, 16, 0, 0, 0, 
            1, 0,                       // type
            0, 0,                       // channels
            0, 0, 0, 0,                 // samples per second
            0, 0, 0, 0,                 // bytes per second
            0, 0,                       // frame size
            0, 0,                       // bits per sample
            0x64, 0x61, 0x74, 0x61,
            0, 0, 0, 0                  // data chunk size
        };

        private byte[] last;
        public override int Read(byte[] buffer, int offset, int count)
        {
            var i = 0;
            if (position < 44)
            {
                i = (int)(44 - position);
                if (i > count) i = count;
                Array.Copy(header, position, buffer, offset, i);
                position = (uint)(position + i);
                offset += i;
                count -= i;
            }
            if (count == 0) return i;

            var j = (int) ((position - 44) % actualBytesPerSample);
            if (j > 0)
            {
                var k = actualBytesPerSample - j;
                if (k > count) k = count;
                Array.Copy(last, j, buffer, offset, k);
                position = (uint) (position + k);
                offset += k;
                count -= k;
                i += k;
            }
            if (count == 0) return i;

            while (count > 0 && position < length)
            {
                var k = project.Update((double)(position - 44) / actualBytesPerSample / samplesPerSecond);
                if (bytesPerSample > 0)
                {
                    var up = 1L << ((bytesPerSample << 3) - 1);
                    var val = Math.Round(k * (up - 1));
                    last = BitConverter.GetBytes(bytesPerSample == 1 ? (long) val + 128
                        : val >= 0 || bytesPerSample >= 8 ? (long) val : up + up + 1 - (long) -val);
                }
                else if (bytesPerSample == -4) last = BitConverter.GetBytes((float) k);
                else if (bytesPerSample == -8) last = BitConverter.GetBytes(k);
                else throw new NotSupportedException("未知的 bytesPerSample！");
                j = actualBytesPerSample;
                if (j > count) j = count;
                Array.Copy(last, 0, buffer, offset, j);
                position = (uint) (position + j);
                offset += j;
                count -= j;
                i += j;
            }
            return i;
        }

        public override void Flush()
        {
        }
        public override long Seek(long offset, SeekOrigin origin)
        {
            throw new NotSupportedException();
        }
        public override void SetLength(long value)
        {
            Array.Copy(BitConverter.GetBytes((uint) value), 0, header, 4, 4);
        }
        public override void Write(byte[] buffer, int offset, int count)
        {
            throw new NotSupportedException();
        }

        public override bool CanRead { get { return true; } }
        public override bool CanSeek { get { return false; } }
        public override bool CanWrite { get { return false; } }
        public override long Length { get { return length; } }
        public override long Position { get { return position; } set { throw new NotSupportedException(); } }
    }
}
