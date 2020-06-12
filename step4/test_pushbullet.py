from pushbullet import Pushbullet

apikey = "o.gpJ6P67e17nBH90711BrCiU1LcR9DUbZ"
pb = Pushbullet(apikey)

push = pb.push_note("RaspberryPi", "push message")  