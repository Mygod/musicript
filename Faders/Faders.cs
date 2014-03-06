using System;

namespace Mygod.Musicript.Volumers.Faders
{
    /// <summary>
    /// 线性衰减器。
    /// </summary>
    public class LinearFader
    {
        private double speed;

        /// <summary>
        /// 设置衰减速度。
        /// </summary>
        /// <param name="value">衰减速度。</param>
        public void SetSpeed(string value)
        {
            speed = double.Parse(value);
        }

        /// <summary>
        /// 控制指定时刻的音量。
        /// </summary>
        /// <param name="time">时刻。</param>
        /// <returns>指定时刻的音量。</returns>
        public double GetVolume(double time)
        {
            var temp = 1 - time * speed;
            return temp < 0 ? 0 : temp;
        }
    }

    /// <summary>
    /// 对数衰减器。
    /// </summary>
    public class LogarithmicFader
    {
        private double speed;

        /// <summary>
        /// 设置衰减速度。
        /// </summary>
        /// <param name="value">衰减速度。</param>
        public void SetSpeed(string value)
        {
            speed = double.Parse(value);
        }

        /// <summary>
        /// 控制指定时刻的音量。
        /// </summary>
        /// <param name="time">时刻。</param>
        /// <returns>指定时刻的音量。</returns>
        public double GetVolume(double time)
        {
            return Math.Exp(-time * speed);
        }
    }
}
