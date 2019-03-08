# Audio Recording

## Recording API: [MediaRecorder](https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder)
* Compatibility
    * [x] Desktop
      * [x] Chrome
      * [x] Firefox
      * [x] Opera
    * [x] Android
      * [x] Android Webview
      * [x] Chrome
      * [x] Firefox
      * [x] Opera
    * [ ] iOS - compatibility unknown
      * [ ] Safari
* Output format - PCM (uncompressed)

## Next Steps
* Wrap PCM data in WAV container
* Send WAV to cloud for transcription
* Chunk audio at meaningful breakpoints
  * For example, break when no one is speaking for a period of time.

## Resources
### Intro to Audio formatting
  * [Codecs and Formats](https://support.brightcove.com/zencoder-faq-codecs-and-formats)
  * [File formats and data compression](https://guides.vpl.ca/c.php?g=698623&p=4959588)
### Putting PCM data into a WAV container
  * [WAV PCM format](http://soundfile.sapp.org/doc/WaveFormat/)
  * [Reading PCM audio with Python](https://www.swharden.com/wp/2009-06-19-reading-pcm-audio-with-python/)
  * [Add WAV-header to PCM data](https://gist.github.com/dasuxullebt/10012305)
### Examples
* [Example using MediaStream Recording API](https://developer.mozilla.org/en-US/docs/Web/API/MediaStream_Recording_API/Using_the_MediaStream_Recording_API)
### Support
* [MediaRecorder Polyfill for iOS support](https://blog.addpipe.com/recording-audio-in-the-browser-using-pure-html5-and-minimal-javascript/)
### Miscellaneous
* [Spectrum Analyzer](https://academo.org/demos/spectrum-analyzer/)
