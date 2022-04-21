import React, { useRef, useState, useEffect } from 'react'

const AudioPlayer = ({ audioScr }) => {

  const music = useRef(new Audio(audioScr))
  const seekbar = useRef()

  const [currentTimeDisplay, setCurrentTimeDisplay] = useState('0:00')
  const [durationDisplay, setDurationDisplay] = useState('0:00')
  const [isPlaying, setIsPlaying] = useState(false)
  const [duration, setDuration] = useState(100)

  const handlePlay = () => setIsPlaying(playing => !playing)

  const onSrub = (e) => {
      music.current.currentTime = e.target.value;
  }

  useEffect(() => {
    if (isPlaying) {
      music.current.play();
    }
    else {
      music.current.pause();
    }
  }, [isPlaying])

  useEffect(() => {
    music.current.ontimeupdate = () => {
      const csec = parseInt(music.current.currentTime % 60);
      const cmin = parseInt((music.current.currentTime / 60) % 60);
      const currentSec = csec < 10 ? `0${csec}` : csec;
      setCurrentTimeDisplay(cmin + ':' + currentSec);
    }
  }, [])

  useEffect(() => {
      console.log({duration:music.current.duration})
    if (parseInt(music.current.duration)) {
      const ds = parseInt(music.current.duration % 60);
      const dm = parseInt((music.current.duration / 60) % 60);
      setDurationDisplay(dm + ':' + ds);
      setDuration(music.current.duration);
    }
    else {
      setDurationDisplay('0:00');
      setDuration(100);
    }
  }, [music.current.duration])

 
  useEffect(() => {
    if (music.current.ended) {
      setIsPlaying(false);
    }
  }, [music.current.ended])

  return (
    <div className="d-flex justify-content-center pt-6">
      <div className="et-audioPlayer">
        <div className="et-musicBox">
          <div className="et-musicBar px-3 pt-13 pb-20">
            <span className="et-currentTime px-2">{currentTimeDisplay}</span>
            <input type="range" step="1" ref={seekbar} value={Math.floor(music.current.currentTime)} onChange={onSrub} min="0"  max={Math.floor(duration)} ></input>
            <span className="et-duration px-2">{durationDisplay}</span>
          </div>
          <span className="et-audioPlay px-11 py-19" onClick={handlePlay}>
            <i >{isPlaying ? <i className='et-pause' /> : <i className='et-play' />}</i>
          </span>
        </div>
      </div>
    </div>
  );
}

export default AudioPlayer;
