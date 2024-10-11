"""
Audaspace (pronounced "outer space") is a high level audio library.


--------------------

This script shows how to use the classes: Device, Factory and
Handle.

```../examples/aud.py```

"""

import typing
import collections.abc
import typing_extensions

class Device:
    """Device objects represent an audio output backend like OpenAL or SDL, but might also represent a file output or RAM buffer output.lock()Locks the device so that it's guaranteed, that no samples are read from the streams until `unlock` is called.
    This is useful if you want to do start/stop/pause/resume some sounds at the same time.play(sound, keep=False)Plays a sound.stopAll()Stops all playing and paused sounds.unlock()Unlocks the device after a lock call, see `lock` for details.
    """

    channels: typing.Any
    """ The channel count of the device."""

    distance_model: typing.Any
    """ The distance model of the device.http://connect.creativelabs.com/openal/Documentation/OpenAL%201.1%20Specification.htm#_Toc199835864"""

    doppler_factor: typing.Any
    """ The doppler factor of the device.
This factor is a scaling factor for the velocity vectors in doppler calculation. So a value bigger than 1 will exaggerate the effect as it raises the velocity."""

    format: typing.Any
    """ The native sample format of the device."""

    listener_location: typing.Any
    """ The listeners's location in 3D space, a 3D tuple of floats."""

    listener_orientation: typing.Any
    """ The listener's orientation in 3D space as quaternion, a 4 float tuple."""

    listener_velocity: typing.Any
    """ The listener's velocity in 3D space, a 3D tuple of floats."""

    rate: typing.Any
    """ The sampling rate of the device in Hz."""

    speed_of_sound: typing.Any
    """ The speed of sound of the device.
The speed of sound in air is typically 343.3 m/s."""

    volume: typing.Any
    """ The overall volume of the device."""

class DynamicMusic:
    """The DynamicMusic object allows to play music depending on a current scene, scene changes are managed by the class, with the possibility of custom transitions.
    The default transition is a crossfade effect, and the default scene is silent and has id 0addScene(scene)Adds a new scene.addTransition(ini, end, transition)Adds a new scene.pause()Pauses playback of the scene.resume()Resumes playback of the scene.stop()Stops playback of the scene.
    """

    fadeTime: typing.Any
    """ The length in seconds of the crossfade transition"""

    position: typing.Any
    """ The playback position of the scene in seconds."""

    scene: typing.Any
    """ The current scene"""

    status: typing.Any
    """ Whether the scene is playing, paused or stopped (=invalid)."""

    volume: typing.Any
    """ The volume of the scene."""

class Handle:
    """Handle objects are playback handles that can be used to control playback of a sound. If a sound is played back multiple times then there are as many handles.pause()Pauses playback.resume()Resumes playback.stop()Stops playback."""

    attenuation: typing.Any
    """ This factor is used for distance based attenuation of the source.:attr:`Device.distance_model`"""

    cone_angle_inner: typing.Any
    """ The opening angle of the inner cone of the source. If the cone values of a source are set there are two (audible) cones with the apex at the `location` of the source and with infinite height, heading in the direction of the source's `orientation`.
In the inner cone the volume is normal. Outside the outer cone the volume will be `cone_volume_outer` and in the area between the volume will be interpolated linearly."""

    cone_angle_outer: typing.Any
    """ The opening angle of the outer cone of the source.:attr:`cone_angle_inner`"""

    cone_volume_outer: typing.Any
    """ The volume outside the outer cone of the source.:attr:`cone_angle_inner`"""

    distance_maximum: typing.Any
    """ The maximum distance of the source.
If the listener is further away the source volume will be 0.:attr:`Device.distance_model`"""

    distance_reference: typing.Any
    """ The reference distance of the source.
At this distance the volume will be exactly `volume`.:attr:`Device.distance_model`"""

    keep: typing.Any
    """ Whether the sound should be kept paused in the device when its end is reached.
This can be used to seek the sound to some position and start playback again."""

    location: typing.Any
    """ The source's location in 3D space, a 3D tuple of floats."""

    loop_count: typing.Any
    """ The (remaining) loop count of the sound. A negative value indicates infinity."""

    orientation: typing.Any
    """ The source's orientation in 3D space as quaternion, a 4 float tuple."""

    pitch: typing.Any
    """ The pitch of the sound."""

    position: typing.Any
    """ The playback position of the sound in seconds."""

    relative: typing.Any
    """ Whether the source's location, velocity and orientation is relative or absolute to the listener."""

    status: typing.Any
    """ Whether the sound is playing, paused or stopped (=invalid)."""

    velocity: typing.Any
    """ The source's velocity in 3D space, a 3D tuple of floats."""

    volume: typing.Any
    """ The volume of the sound."""

    volume_maximum: typing.Any
    """ The maximum volume of the source.:attr:`Device.distance_model`"""

    volume_minimum: typing.Any
    """ The minimum volume of the source.:attr:`Device.distance_model`"""

class PlaybackManager:
    """A PlabackManager object allows to easily control groups os sounds organized in categories.addCategory(volume)Adds a category with a custom volume.clean()Cleans all the invalid and finished sound from the playback manager.getVolume(catKey)Retrieves the volume of a category.pause(catKey)Pauses playback of the category.setVolume(sound, catKey)Plays a sound through the playback manager and assigns it to a category.resume(catKey)Resumes playback of the catgory.setVolume(volume, catKey)Changes the volume of a category.stop(catKey)Stops playback of the category."""

class Sequence:
    """This sound represents sequenced entries to play a sound sequence.add()Adds a new entry to the sequence.remove()Removes an entry from the sequence.setAnimationData()Writes animation data to a sequence."""

    channels: typing.Any
    """ The channel count of the sequence."""

    distance_model: typing.Any
    """ The distance model of the sequence.http://connect.creativelabs.com/openal/Documentation/OpenAL%201.1%20Specification.htm#_Toc199835864"""

    doppler_factor: typing.Any
    """ The doppler factor of the sequence.
This factor is a scaling factor for the velocity vectors in doppler calculation. So a value bigger than 1 will exaggerate the effect as it raises the velocity."""

    fps: typing.Any
    """ The listeners's location in 3D space, a 3D tuple of floats."""

    muted: typing.Any
    """ Whether the whole sequence is muted."""

    rate: typing.Any
    """ The sampling rate of the sequence in Hz."""

    speed_of_sound: typing.Any
    """ The speed of sound of the sequence.
The speed of sound in air is typically 343.3 m/s."""

class SequenceEntry:
    """SequenceEntry objects represent an entry of a sequenced sound.move()Moves the entry.setAnimationData()Writes animation data to a sequenced entry."""

    attenuation: typing.Any
    """ This factor is used for distance based attenuation of the source.:attr:`Device.distance_model`"""

    cone_angle_inner: typing.Any
    """ The opening angle of the inner cone of the source. If the cone values of a source are set there are two (audible) cones with the apex at the `location` of the source and with infinite height, heading in the direction of the source's `orientation`.
In the inner cone the volume is normal. Outside the outer cone the volume will be `cone_volume_outer` and in the area between the volume will be interpolated linearly."""

    cone_angle_outer: typing.Any
    """ The opening angle of the outer cone of the source.:attr:`cone_angle_inner`"""

    cone_volume_outer: typing.Any
    """ The volume outside the outer cone of the source.:attr:`cone_angle_inner`"""

    distance_maximum: typing.Any
    """ The maximum distance of the source.
If the listener is further away the source volume will be 0.:attr:`Device.distance_model`"""

    distance_reference: typing.Any
    """ The reference distance of the source.
At this distance the volume will be exactly `volume`.:attr:`Device.distance_model`"""

    muted: typing.Any
    """ Whether the entry is muted."""

    relative: typing.Any
    """ Whether the source's location, velocity and orientation is relative or absolute to the listener."""

    sound: typing.Any
    """ The sound the entry is representing and will be played in the sequence."""

    volume_maximum: typing.Any
    """ The maximum volume of the source.:attr:`Device.distance_model`"""

    volume_minimum: typing.Any
    """ The minimum volume of the source.:attr:`Device.distance_model`"""

class Sound:
    """Sound objects are immutable and represent a sound that can be played simultaneously multiple times. They are called factories because they create reader objects internally that are used for playback.buffer(data, rate)Creates a sound from a data buffer.file(filename)Creates a sound object of a sound file.list()Creates an empty sound list that can contain several sounds.sawtooth(frequency, rate=48000)Creates a sawtooth sound which plays a sawtooth wave.silence(rate=48000)Creates a silence sound which plays simple silence.sine(frequency, rate=48000)Creates a sine sound which plays a sine wave.square(frequency, rate=48000)Creates a square sound which plays a square wave.triangle(frequency, rate=48000)Creates a triangle sound which plays a triangle wave.ADSR(attack,decay,sustain,release)Attack-Decay-Sustain-Release envelopes the volume of a sound. Note: there is currently no way to trigger the release with this API.accumulate(additive=False)Accumulates a sound by summing over positive input differences thus generating a monotonic sigal. If additivity is set to true negative input differences get added too, but positive ones with a factor of two. Note that with additivity the signal is not monotonic anymore.addSound(sound)Adds a new sound to a sound list.cache()Caches a sound into RAM.
    This saves CPU usage needed for decoding and file access if the underlying sound reads from a file on the harddisk, but it consumes a lot of memory.data()Retrieves the data of the sound as numpy array.delay(time)Delays by playing adding silence in front of the other sound's data.envelope(attack, release, threshold, arthreshold)Delays by playing adding silence in front of the other sound's data.fadein(start, length)Fades a sound in by raising the volume linearly in the given time interval.fadeout(start, length)Fades a sound in by lowering the volume linearly in the given time interval.filter(b, a = (1))Filters a sound with the supplied IIR filter coefficients.
    Without the second parameter you'll get a FIR filter.
    If the first value of the a sequence is 0 it will be set to 1 automatically.
    If the first value of the a sequence is neither 0 nor 1, all filter coefficients will be scaled by this value so that it is 1 in the end, you don't have to scale yourself.highpass(frequency, Q=0.5)Creates a second order highpass filter based on the transfer function H(s) = s^2 / (s^2 + s/Q + 1)join(sound)Plays two factories in sequence.limit(start, end)Limits a sound within a specific start and end time.loop(count)Loops a sound.lowpass(frequency, Q=0.5)Creates a second order lowpass filter based on the transfer function H(s) = 1 / (s^2 + s/Q + 1)mix(sound)Mixes two factories.modulate(sound)Modulates two factories.mutable()Creates a sound that will be restarted when sought backwards.
    If the original sound is a sound list, the playing sound can change.pingpong()Plays a sound forward and then backward.
    This is like joining a sound with its reverse.pitch(factor)Changes the pitch of a sound with a specific factor.rechannel(channels)Rechannels the sound.resample(rate, high_quality)Resamples the sound.reverse()Plays a sound reversed.sum()Sums the samples of a sound.threshold(threshold = 0)Makes a threshold wave out of an audio wave by setting all samples with a amplitude >= threshold to 1, all <= -threshold to -1 and all between to 0.volume(volume)Changes the volume of a sound.write(filename, rate, channels, format, container, codec, bitrate, buffersize)Writes the sound to a file.
    """

    length: typing.Any
    """ The sample specification of the sound as a tuple with rate and channel count."""

    specs: typing.Any
    """ The sample specification of the sound as a tuple with rate and channel count."""

class Source:
    """The source object represents the source position of a binaural sound."""

    azimuth: typing.Any
    """ The azimuth angle."""

    distance: typing.Any
    """ The distance value. 0 is min, 1 is max."""

    elevation: typing.Any
    """ The elevation angle."""

class ThreadPool:
    """A ThreadPool is used to parallelize convolution efficiently."""

class error: ...

AP_LOCATION: typing.Any
""" constant value 3
"""

AP_ORIENTATION: typing.Any
""" constant value 4
"""

AP_PANNING: typing.Any
""" constant value 1
"""

AP_PITCH: typing.Any
""" constant value 2
"""

AP_VOLUME: typing.Any
""" constant value 0
"""

CHANNELS_INVALID: typing.Any
""" constant value 0
"""

CHANNELS_MONO: typing.Any
""" constant value 1
"""

CHANNELS_STEREO: typing.Any
""" constant value 2
"""

CHANNELS_STEREO_LFE: typing.Any
""" constant value 3
"""

CHANNELS_SURROUND4: typing.Any
""" constant value 4
"""

CHANNELS_SURROUND5: typing.Any
""" constant value 5
"""

CHANNELS_SURROUND51: typing.Any
""" constant value 6
"""

CHANNELS_SURROUND61: typing.Any
""" constant value 7
"""

CHANNELS_SURROUND71: typing.Any
""" constant value 8
"""

CODEC_AAC: typing.Any
""" constant value 1
"""

CODEC_AC3: typing.Any
""" constant value 2
"""

CODEC_FLAC: typing.Any
""" constant value 3
"""

CODEC_INVALID: typing.Any
""" constant value 0
"""

CODEC_MP2: typing.Any
""" constant value 4
"""

CODEC_MP3: typing.Any
""" constant value 5
"""

CODEC_OPUS: typing.Any
""" constant value 8
"""

CODEC_PCM: typing.Any
""" constant value 6
"""

CODEC_VORBIS: typing.Any
""" constant value 7
"""

CONTAINER_AC3: typing.Any
""" constant value 1
"""

CONTAINER_FLAC: typing.Any
""" constant value 2
"""

CONTAINER_INVALID: typing.Any
""" constant value 0
"""

CONTAINER_MATROSKA: typing.Any
""" constant value 3
"""

CONTAINER_MP2: typing.Any
""" constant value 4
"""

CONTAINER_MP3: typing.Any
""" constant value 5
"""

CONTAINER_OGG: typing.Any
""" constant value 6
"""

CONTAINER_WAV: typing.Any
""" constant value 7
"""

DISTANCE_MODEL_EXPONENT: typing.Any
""" constant value 5
"""

DISTANCE_MODEL_EXPONENT_CLAMPED: typing.Any
""" constant value 6
"""

DISTANCE_MODEL_INVALID: typing.Any
""" constant value 0
"""

DISTANCE_MODEL_INVERSE: typing.Any
""" constant value 1
"""

DISTANCE_MODEL_INVERSE_CLAMPED: typing.Any
""" constant value 2
"""

DISTANCE_MODEL_LINEAR: typing.Any
""" constant value 3
"""

DISTANCE_MODEL_LINEAR_CLAMPED: typing.Any
""" constant value 4
"""

FORMAT_FLOAT32: typing.Any
""" constant value 36
"""

FORMAT_FLOAT64: typing.Any
""" constant value 40
"""

FORMAT_INVALID: typing.Any
""" constant value 0
"""

FORMAT_S16: typing.Any
""" constant value 18
"""

FORMAT_S24: typing.Any
""" constant value 19
"""

FORMAT_S32: typing.Any
""" constant value 20
"""

FORMAT_U8: typing.Any
""" constant value 1
"""

RATE_11025: typing.Any
""" constant value 11025
"""

RATE_16000: typing.Any
""" constant value 16000
"""

RATE_192000: typing.Any
""" constant value 192000
"""

RATE_22050: typing.Any
""" constant value 22050
"""

RATE_32000: typing.Any
""" constant value 32000
"""

RATE_44100: typing.Any
""" constant value 44100
"""

RATE_48000: typing.Any
""" constant value 48000
"""

RATE_8000: typing.Any
""" constant value 8000
"""

RATE_88200: typing.Any
""" constant value 88200
"""

RATE_96000: typing.Any
""" constant value 96000
"""

RATE_INVALID: typing.Any
""" constant value 0
"""

STATUS_INVALID: typing.Any
""" constant value 0
"""

STATUS_PAUSED: typing.Any
""" constant value 2
"""

STATUS_PLAYING: typing.Any
""" constant value 1
"""

STATUS_STOPPED: typing.Any
""" constant value 3
"""
