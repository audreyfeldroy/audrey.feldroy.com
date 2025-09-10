# Alarm Sounds App

Demo of adding sounds to a FastHTML app with Tone.js. Sounds make web apps come alive and feel interactive.

Here I notebookify and improve [alarmsounds](https://github.com/audreyfeldroy/alarmsounds/blob/main/main.py).

## Setup


```python
from fasthtml.common import *
from fasthtml.jupyter import *
from monsterui.all import *
```


```python
app, rt = fast_app(hdrs=(Theme.slate.headers(), Script(src="https://unpkg.com/tone")))
```

## The Sounds


```python
beeping_sounds = (
    ("Classic", "Repeating beeps", """const synth = new Tone.Synth().toDestination();
        const loopA = new Tone.Loop((time) => {
            synth.triggerAttackRelease("C5", "16n");
        }, "4n").start(0);
     Tone.getTransport().start();"""),
        
    ("Digital Beep", "Modern digital alarm", """
        const synth = new Tone.Synth({
            oscillator: {type: "square"},
            envelope: {attack: 0.001, decay: 0.1, sustain: 1, release: 0.1}
        }).toDestination();
        
        const loop = new Tone.Loop(time => {
            synth.triggerAttackRelease("C6", "16n");
        }, "0.25").start(0);
        
        Tone.Transport.start();"""),
    
    ("Pulsing Alarm", "Pulsing alarm with rising intensity", """
        const pulseA = new Tone.Synth({
            oscillator: {type: "triangle"},
            envelope: {attack: 0.01, decay: 0.3, sustain: 0.1, release: 0.1}
        }).toDestination();
        pulseA.volume.value = -12;

        const pulseB = new Tone.Synth({
            oscillator: {type: "square"},
            envelope: {attack: 0.01, decay: 0.2, sustain: 0.1, release: 0.1}
        }).toDestination();
        pulseB.volume.value = -20;

        // Start quiet and get louder
        const vol = new Tone.Volume(-20).toDestination();
        pulseA.connect(vol);
        pulseB.connect(vol);
        vol.volume.rampTo(-5, 5);

        const loop = new Tone.Loop(time => {
            pulseA.triggerAttackRelease("E5", "16n", time);
            pulseB.triggerAttackRelease("B5", "16n", time + 0.1);
        }, "0.3").start(0);

        Tone.Transport.start();""")
)
```


```python
musical_sounds = (
    ("Good Morning", "Bright polyphonic tones", """const synth = new Tone.PolySynth(Tone.Synth).toDestination();
        const now = Tone.now();
        synth.triggerAttack("D4", now);
        synth.triggerAttack("F4", now + 0.5);
        synth.triggerAttack("A4", now + 1);
        synth.triggerAttack("C5", now + 1.5);
        synth.triggerAttack("E5", now + 2);
        synth.triggerRelease(["D4", "F4", "A4", "C5", "E5"], now + 4);"""),
    ("Metallophone", "Striking metal", """
        const bell = new Tone.MetalSynth({
            frequency: 150,
            envelope: {
                attack: 0.001,
                decay: 2.0,
                release: 0.8
            },
            harmonicity: 12,
            modulationIndex: 20,
            resonance: 1000,
            octaves: 1.2
        }).toDestination();
        
        const loop = new Tone.Loop(time => {
            bell.triggerAttackRelease("32n", time);
        }, "0.4").start(0);
        
        Tone.Transport.start();"""),

)
```


```python
nature_sounds = (
        
    ("Forest Morning", "Birds and rustling leaves", """
        // Bird chirps
        const bird1 = new Tone.FMSynth({
            modulationIndex: 10,
            envelope: {attack: 0.001, decay: 0.1}
        }).toDestination();
        const bird2 = new Tone.FMSynth({
            modulationIndex: 8,
            envelope: {attack: 0.001, decay: 0.08}
        }).toDestination();
        
        // Leaves rustling (filtered noise)
        const noise = new Tone.Noise("pink").toDestination();
        noise.volume.value = -30;
        const filter = new Tone.Filter({
            frequency: 2000,
            type: "highpass"
        }).toDestination();
        noise.connect(filter);
        
        // Random bird calls
        const birdLoop = new Tone.Loop(time => {
            const notes = ["E6", "G6", "A6"];
            bird1.triggerAttackRelease(notes[Math.floor(Math.random() * notes.length)], "16n");
            if(Math.random() > 0.7) {
                bird2.triggerAttackRelease("C7", "32n", "+0.1");
            }
        }, "4n").start();
        
        noise.start();
        Tone.Transport.start();"""),
        
    ("Mountain Stream", "Bubbling water and morning birds", """
        // Water sounds
        const water = new Tone.Noise("white").toDestination();
        water.volume.value = -25;
        const waterFilter = new Tone.Filter({
            frequency: 1000,
            type: "bandpass",
            Q: 2
        }).toDestination();
        water.connect(waterFilter);
        
        // Occasional bird chirps
        const bird = new Tone.Synth({
            oscillator: {type: "triangle"},
            envelope: {attack: 0.001, decay: 0.1, sustain: 0, release: 0.1}
        }).toDestination();
        
        const birdLoop = new Tone.Loop(time => {
            if(Math.random() > 0.8) {
                const note = Math.random() > 0.5 ? "E6" : "G6";
                bird.triggerAttackRelease(note, "16n");
                bird.triggerAttackRelease(note, "16n", "+0.1");
            }
        }, "2n").start();
        
        water.start();
        Tone.Transport.start();""")
)
```


```python
emergency_sounds = (
    ("Fire Alarm", "Standard emergency siren", """
        const synth = new Tone.Synth({
            oscillator: {type: "sawtooth"},
            envelope: {attack: 0.01, decay: 0.1, sustain: 1, release: 0.1}
        }).toDestination();
        
        let pitch = true;
        const loop = new Tone.Loop(time => {
            synth.triggerAttackRelease(pitch ? "C5" : "G5", "0.25");
            pitch = !pitch;
        }, "0.25").start(0);
        
        Tone.Transport.start();"""),

)
```


```python
def MusicLi(t,hk=''): return Li(A(DivFullySpaced(t,P(hk,cls=TextFont.muted_sm))))
```


```python
def Album(title,artist,scr):
    return Div(
        Div(
            UkIcon('alarm-clock', height=150, width=150,
                cls="transition-transform duration-200 hover:scale-105", 
                onmousedown=scr),
            cls="overflow-hidden rounded-md"),
        Div(cls='space-y-1')(P(title,cls=TextT.bold),P(artist,cls=TextT.muted)))
```

## Tabs

Currently the app only has an Alarms tab:

I'm not using these at the moment but may re-add them in later, or I may just remove them:


```python
def Tab(title, desc, sounds):
    return (
        Div(H2(title), cls="mt-6 space-y-1"),
                    P(desc, cls=TextFont.muted_sm),
                    DividerLine(),
                    Grid(*[Album(t,a,s) for t,a,s in sounds], cls='gap-8'))
```


```python
def BeepingTab():
    return Tab("Beeping", "Listen to your favorite beeping alarm clock sounds.", beeping_sounds)
```


```python
def MusicalTab():
    return Tab("Musical", "Alarm sounds that add music to your waking experience.", musical_sounds)
```


```python
def NatureTab():
    return Tab("Nature", "Wake up to nature-inspired sounds.", nature_sounds)
```


```python
def EmergencyTab():
    return Tab("Emergency", "Startle yourself out of bed with emergency-inspired sounds.", emergency_sounds)
```

## Main Page


```python
@rt('/')
def page():
    return Container(
            H1("Alarm Sounds", cls="mb-6"),
            Div(cls="col-span-4")(
                Div(
                    DivFullySpaced(
                        Div(
                            TabContainer(
                                Li(A('Beeping', href='#'), cls='uk-active'),
                                Li(A('Musical',    href='#'),
                                Li(A('Nature'), href='#'),
                                Li(A('Emergency'), href='#')),
                                uk_switcher='connect: #component-nav; animation: uk-animation-fade',
                                alt=True), 
                            cls="max-w-80"),
                    ),
                    Ul(
                        Li(BeepingTab()),
                        Li(MusicalTab()),
                        Li(NatureTab()),
                        Li(EmergencyTab()),
                        id="component-nav", 
                        cls="uk-switcher")
                )
            ),
            cols=5)
```

## Serve


```python
server = JupyUvi(app)
```

    ERROR:    [Errno 48] error while attempting to bind on address ('0.0.0.0', 8000): [errno 48] address already in use


## Show App in This Notebook


```python
# HTMX(page, height=500)
```

## Stop


```python
server.stop()
```

## Next Steps

* This is shaping up enough that I think I'll bring it back to the https://github.com/audreyfeldroy/alarmsounds/ repo.
* It needs refactoring
* Currently you have to refresh the page to stop sounds. It would be nice if when you click a button, it's pressed down until you turn it off.
