using System;

namespace Mygod.Musicript.Pitchers.Oscillators
{
    /// <summary>
    /// 线性正弦波振荡。
    /// </summary>
    public class LinearSineWaveOscillator
    {
        private static double oscillationFrequency, oscillationAmplitude;

        /// <summary>
        /// 设置振频。
        /// </summary>
        /// <param name="value"></param>
        public void SetFrequency(string value)
        {
            oscillationFrequency = double.Parse(value);
        }

        /// <summary>
        /// 设置振幅。
        /// </summary>
        /// <param name="value"></param>
        public void SetAmplitude(string value)
        {
            oscillationAmplitude = double.Parse(value);
        }

        /// <summary>
        /// 变调。
        /// </summary>
        /// <param name="frequency">原频率。</param>
        /// <param name="time">时刻。</param>
        /// <returns>变调后映射到的时刻。</returns>
        public double Pitch(double frequency, double time)
        {
            var temp = 2 * Math.PI * oscillationFrequency;
            return frequency * time + (1 - Math.Cos(temp * time)) * oscillationAmplitude / temp;
        }
    }
}
