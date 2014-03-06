using System;

namespace Mygod.Musicript.Pitchers.Inflection
{
    /// <summary>
    /// 线性变调。
    /// </summary>
    public sealed class LinearInflection
    {
        private static double speed;

        /// <summary>
        /// 设置变调速度。
        /// </summary>
        /// <param name="value"></param>
        public void SetSpeed(string value)
        {
            speed = double.Parse(value);
        }

        /// <summary>
        /// 变调。
        /// </summary>
        /// <param name="frequency">原频率。</param>
        /// <param name="time">时刻。</param>
        /// <returns>变调后映射到的时刻。</returns>
        public double Pitch(double frequency, double time)
        {
            var result = time * (frequency + speed * time / 2);
            if (speed >= 0) return result;
            var temp = -frequency / speed;
            return time > temp ? temp * frequency / 2 : result;
        }
    }

    /// <summary>
    /// 对数变调。
    /// </summary>
    public sealed class LogarithmicInflection
    {
        private static double speed;

        /// <summary>
        /// 设置变调速度。
        /// </summary>
        /// <param name="value"></param>
        public void SetSpeed(string value)
        {
            speed = double.Parse(value);
        }

        /// <summary>
        /// 变调。
        /// </summary>
        /// <param name="frequency">原频率。</param>
        /// <param name="time">时刻。</param>
        /// <returns>变调后映射到的时刻。</returns>
        public double Pitch(double frequency, double time)
        {
            if (Math.Abs(speed) < 1e-8) return frequency * time;
                                        // no inflection
            return frequency * (Math.Exp(speed * time) - 1) / speed;
        }
    }
}
