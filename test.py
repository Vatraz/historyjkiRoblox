from historyki_roblox.actor_factory import ActorFactory
from historyki_roblox.video.video_builder import VideoBuilder

actor_factory = ActorFactory()

characters = [
    ('Bartosz', 'MALE','data/images/alien.png'),
    ('Robert', 'MALE','data/images/robbcio.png'),
    ('Krystyna', 'FEMALE','data/images/mc.png'),
    ('Friz', 'MALE','data/images/pawel.png'),
]

n, actors = 0, {}
for name, gender, image in characters:
    actor = actor_factory.create_actor(name, n, gender, image)
    actors[name] = actor
    n += 1

video_builder = VideoBuilder('data/stories/test_data/0.txt', actors)
video_builder.add_background_video('steven.webm')
video_builder.add_story_elements_to_video()
video_builder.save()
