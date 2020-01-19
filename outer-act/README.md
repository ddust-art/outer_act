# outer-act
Test code for interactive video with camera motion detection

Fixes necessary to the actual code:

1. Animation Loop:
The animation doesn't start at the right point when triggered by the camera's motion detection. Each image sequence from the lists, should start from the initial fram defined in "image_frames".

2. Animations' length:
The "self.anim_length" should have variable values, because each animation will have a distinct duration.

3. Score:
The "def update score" has to be changed". Each animation/ image sequence should be triggered by the camera's motion detection in a continuos loop, but never repeating an animation within a cycle. When the last animation reaches it's end, then the script reset's itself. The following motion detection will trigger again the first animation and so on, as in a cycle.

4. Audio tracks:
The actual code uses the "whatsupbro.wav" file for testing audio. As each animation will have a different audio track, that means that each audio file has to be triggered together with it's correspondent animation. Another audio file was put on the "audio" folder for experimentation.


Please, if necessary check more explanations about the motion detection's code: 
 https://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/

For the Pyglet library and animation methods, check the library' documentation at:
https://pyglet.readthedocs.io/en/stable/

