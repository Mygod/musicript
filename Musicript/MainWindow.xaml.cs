using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.Windows;
using IrrKlang;
using Microsoft.Win32;
using Microsoft.WindowsAPICodePack.Dialogs;
using Mygod.Net;
using Mygod.Windows;

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
        private readonly SaveFileDialog wavSaver = new SaveFileDialog
            { Filter = "波形文件 (*.wav) | *.wav", AddExtension = true };

        private static readonly ISoundEngine Engine = new ISoundEngine();
        private static ISound sound;
        private static int index;
        private static readonly ISoundStopEventReceiver
            Receiver = new SoundStopEventReceiver();

        private void BrowseProject(object sender, RoutedEventArgs e)
        {
            if (projectPicker.ShowDialog(this) == true) ProjectBox.Text = projectPicker.FileName;
        }

        private void ShowMessage(Project proj, ProjectWavStream stream)
        {
            DetailsText.Text = $"{proj.Name} - {proj.Composer} ({proj.Editor} 制作)";
            OverflowText.Text = $"上溢 {stream.OverflowCount} 次，下溢 {stream.UnderflowCount} 次。";
        }

        private void Play(object sender, RoutedEventArgs e)
        {
            if (sound != null) Stop(sender, e);
            var proj = new Project(ProjectBox.Text);
            var stream = proj.Compile(BitsPerSampleBox.SelectedIndex >= 8 ? (BitsPerSampleBox.SelectedIndex - 8) << 2
                                        : (BitsPerSampleBox.SelectedIndex + 1), uint.Parse(SamplingRateBox.Text));
            sound = Engine.Play2D(Engine.AddSoundSourceFromIOStream(stream,
                (++index).ToString(CultureInfo.InvariantCulture)), proj.Looped, false, false);
            sound.setSoundStopEventReceiver(Receiver);
            StopButton.IsEnabled = true;
            ShowMessage(proj, stream);
        }

        private void Stop(object sender, RoutedEventArgs e)
        {
            Engine.StopAllSounds();
            StopButton.IsEnabled = false;
            sound = null;
        }

        private void SaveToFile(object sender, RoutedEventArgs e)
        {
            wavSaver.FileName =
                Path.GetFileNameWithoutExtension(ProjectBox.Text) + ".wav";
            if (wavSaver.ShowDialog(this) != true) return;
            var proj = new Project(ProjectBox.Text);
            using (var input = proj.Compile(BitsPerSampleBox.SelectedIndex >= 8
                        ? (BitsPerSampleBox.SelectedIndex - 7) << 2 : (BitsPerSampleBox.SelectedIndex + 1),
                    uint.Parse(SamplingRateBox.Text)))
            {
                using (var output = new FileStream(wavSaver.FileName, FileMode.Create,
                                                   FileAccess.Write, FileShare.Read)) input.CopyTo(output);
                ShowMessage(proj, input);
            }
        }

        private void Help(object sender, RoutedEventArgs e)
        {
            Process.Start("http://mygod.tk/product/musicript/");
        }

        private void CheckForUpdates(object sender, RoutedEventArgs e)
        {
            WebsiteManager.CheckForUpdates(
                () => TaskDialog.Show(this, "信息", "没有可用的更新。", type: TaskDialogType.Information),
                exc => TaskDialog.Show(this, "错误", "检查更新失败。", type: TaskDialogType.Error,
                                       expandedInfo: exc.GetMessage()));
        }
    }
}
