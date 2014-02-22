using System.Globalization;
using System.IO;
using System.Windows;
using IrrKlang;
using Mygod.Windows;
using Mygod.Windows.Dialogs;

namespace Mygod.Musicript
{
    public sealed partial class MainWindow
    {
        private sealed class SoundStopEventReceiver : ISoundStopEventReceiver
        {
            public void OnSoundStopped(ISound iSound, StopEventCause reason, object userData)
            {
                sound = null;
            }
        }

        public MainWindow()
        {
            InitializeComponent();
        }

        private readonly OpenFileDialog projectPicker = new OpenFileDialog
        {
            InitialDirectory = Path.Combine(CurrentApp.Directory, "Presets", "Sample Projects"),
            Filter = "Musicript 工程 (*.mcp)|*.mcp"
        };
        private readonly SaveFileDialog wavSaver = new SaveFileDialog { Filter = "波形文件 (*.wav) | *.wav", AddExtension = true };

        private static readonly ISoundEngine Engine = new ISoundEngine();
        private static ISound sound;
        private static int index;
        private static readonly ISoundStopEventReceiver Receiver = new SoundStopEventReceiver();

        private void BrowseProject(object sender, RoutedEventArgs e)
        {
            if (projectPicker.ShowDialog(this) == true) ProjectBox.Text = projectPicker.FileName;
        }

        private void Play(object sender, RoutedEventArgs e)
        {
            if (sound != null) Stop(sender, e);
            var proj = new Project(ProjectBox.Text);
            sound = Engine.Play2D(Engine.AddSoundSourceFromIOStream(proj.Compile(BitsPerSampleBox.SelectedIndex >= 8
                ? (BitsPerSampleBox.SelectedIndex - 8) << 2 : (BitsPerSampleBox.SelectedIndex + 1),
                uint.Parse(SamplingRateBox.Text)), (++index).ToString(CultureInfo.InvariantCulture)), proj.Looped, false, false);
            sound.setSoundStopEventReceiver(Receiver);
            StopButton.IsEnabled = true;
        }

        private void Stop(object sender, RoutedEventArgs e)
        {
            Engine.StopAllSounds();
            StopButton.IsEnabled = false;
            sound = null;
        }

        private void SaveToFile(object sender, RoutedEventArgs e)
        {
            wavSaver.FileName = Path.GetFileNameWithoutExtension(ProjectBox.Text) + ".wav";
            if (wavSaver.ShowDialog(this) != true) return;
            var proj = new Project(ProjectBox.Text);
            using (var input = proj.Compile(BitsPerSampleBox.SelectedIndex >= 8 ? (BitsPerSampleBox.SelectedIndex - 7) << 2
                                                : (BitsPerSampleBox.SelectedIndex + 1), uint.Parse(SamplingRateBox.Text)))
            using (var output = new FileStream(wavSaver.FileName, FileMode.Create, FileAccess.Write, FileShare.Read))
                input.CopyTo(output);
        }
    }
}
