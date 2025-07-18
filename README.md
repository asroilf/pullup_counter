# Pull-up Counter Bot

It is a bot that gets the user videos of doing pull-ups and produces the number of reps in the video 

#### Key Tools Used:
MediaPipe, Telegram, peewee, Open-cv, Sqlite3, videohash etc.

-----

### Description
Once the bot receives the video, it processes the video through several stages.

#### Pose Detection

For pose detection pre-trained MediaPipe model by Google is used. It detects human body and extracts landmarks of human joints. Once extracted, it numbers them for reference
![mediapipe_landmark](https://ai.google.dev/static/mediapipe/images/solutions/pose_landmarks_index.png)
||                         Landmarks:                          ||
|--------------------------|--------------------------|--------------------------|
| 0 - nose                 | 11 - left shoulder        | 22 - right thumb         |
| 1 - left eye (inner)     | 12 - right shoulder       | 23 - left hip            |
| 2 - left eye             | 13 - left elbow           | 24 - right hip           |
| 3 - left eye (outer)     | 14 - right elbow          | 25 - left knee           |
| 4 - right eye (inner)    | 15 - left wrist           | 26 - right knee          |
| 5 - right eye            | 16 - right wrist          | 27 - left ankle          |
| 6 - right eye (outer)    | 17 - left pinky           | 28 - right ankle         |
| 7 - left ear             | 18 - right pinky          | 29 - left heel           |
| 8 - right ear            | 19 - left index           | 30 - right heel          |
| 9 - mouth (left)         | 20 - right index          | 31 - left foot index     |
| 10 - mouth (right)       | 21 - left thumb           | 32 - right foot index    |

_source: [google](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker)_

Estracted landmarks in each frame is now ready for analysis. 

### Pull-up Detection
To detect pullups little bit of mathematics and assumption is the main tool. But before applying mathematics, lets first clearify some of the obvious things that a person should have to do pull-ups. 
* To do pull-ups person should be hanging
* To count it as a pull-up shoulders should come close to hands while hanging.
* From biomechanics of a person, when pulled up, degree between wrist-elbow-shoulder and elbow-shuolder-hip should decrease. 
Once the basic physical properties of doing pull-ups is constructed, the entire algorithm can be build arount this idea.
To assume that a person is hanging, we can implement a logic that wrist should be above shoulders for a certain period of time.

Upon detection of hanging position, pull-up moviments are checked. To cancluate angles, `arctan2(wrist-to-elbow) - arctan2(elbow-to-shoulder)` as well as `arcttan2(elbow-to-wrist) - arctan2(shoulder-to-hip)` is calculated. The given degree is then used to assume the pulled-up position. When both degrees are small enough, it is assumed that the person is at pulled position. And when it is not anymore, person has released from that position. 

While hands are released, rep counter adds a rep to its total accumulation.

### 
## Testing Locally


Clone the project

```bash
  git clone https://github.com/asroilf/pullup_counter
```

Go to the project directory

```bash
  cd pullup_counter
```

To run this project it is recommended using docker, since the project requires slightly heavy package installment. 

First thing you should do is specifying telegram bot api key to the Dockerfile

```bash
  ENV PULLUPS_BOT_TOKEN=<TOKEN>
```

Now build an image of a container

```bash
  docker build -t pullup_bot .
```
Upon successful building you should see the following:
```bash
    ...
    Step 10/10 : CMD ["python", "main.py"]
     ---> Running in 679a707447f0
     ---> Removed intermediate container 679a707447f0
     ---> 4b57f95b1cdc
    Successfully built 4b57f95b1cdc
    Successfully tagged pullup_bot:latest
```

Now run the container:
```bash
  docker run pullup_bot
```
The output in the terminal will be:
```bash
    2025-07-15 12:22:05,778 | INFO: Bot is up and running!
```
