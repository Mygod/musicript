using System.IO;
using System.Media;
using System.Windows;
using Mygod.Windows;
using Mygod.Windows.Dialogs;

namespace Mygod.Musicript
{
    public sealed partial class MainWindow
    {
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

        private SoundPlayer player;

        private void BrowseProject(object sender, RoutedEventArgs e)
        {
            if (projectPicker.ShowDialog(this) == true) ProjectBox.Text = projectPicker.FileName;
        }

        private void Play(object sender, RoutedEventArgs e)
        {
            if (player != null) Stop(sender, e);
            var proj = new Project(ProjectBox.Text);
            player = new SoundPlayer(proj.Compile(BitsPerSampleBox.SelectedIndex >= 8
                ? (BitsPerSampleBox.SelectedIndex - 8) << 2 : (BitsPerSampleBox.SelectedIndex + 1),
                uint.Parse(SamplingRateBox.Text))) { LoadTimeout = int.MaxValue };
            if (proj.Looped) player.PlayLooping();
            else player.Play();
            StopButton.IsEnabled = true;
        }

        private void Stop(object sender, RoutedEventArgs e)
        {
            player.Stop();
            player = null;
            StopButton.IsEnabled = false;
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
