import web
from Models import RegisterModel, LoginModel, Events
import datetime

web.config.debug = False

# urls ('path','class')
urls = (
    '/', 'Home',
    '/register', 'Register',
    '/login', 'Login',
    '/logout', 'Logout',
    '/post-registration', 'PostRegistration',
    '/check-login', 'CheckLogin',
    '/addEvent', 'AddEvent',
    '/post-event', 'Post_Event',
    '/events', 'AllEvents',
    '/recent-events', 'RecentEvents',
    '/upcoming-events', 'UpcomingEvents',
    '/my-events', 'MyEvents',
    '/delete/(.*)', 'Delete',
    '/update-events', 'UpdateEvents',
    '/updt/(.*)', 'Updt',
)

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore("sessions"), initializer={"user": None})
session_data = session._initializer

render = web.template.render("Views/Templates", base="MainLayout",
                             globals={'session': session_data, 'current_user': session_data["user"]})


# classes
class Home:
    def GET(self):
        return render.Home()


class UpcomingEvents:
    def GET(self):
        e = Events.Events()
        y = e.upcoming_events()
        return render.UpcomingEvents(y)


class RecentEvents:
    def GET(self):
        e = Events.Events()
        y = e.recent_events()
        return render.RecentEvents(y)


class Register:
    def GET(self):
        return render.Register()


class Login:
    def GET(self):
        return render.Login()


class Delete:
    def POST(self, id):
        y = Events.Events()
        y.del_post(id)
        raise web.seeother('/my-events')


class UpdateEvents:
    def GET(self):
        e = Events.Events()
        u = session_data["user"]["username"]
        events = e.get_events_that_can_be_updated(u)
        print(events)
        return render.Update(events)


class Updt:
    def POST(self, id):
        x = Events.Events()
        data = web.input()
        data.date_updated = datetime.datetime.now()
        x.update_event(id, data)
        raise web.seeother('/my-events')


class MyEvents:
    def GET(self):
        e = Events.Events()
        u = session_data["user"]["username"]
        events = e.get_all_events(u)
        return render.My_events(events)


class PostRegistration:
    def POST(self):
        data = web.input()
        can_use_username = RegisterModel.RegisterModel()
        y = can_use_username.check_username(data)
        if y:
            reg_model = RegisterModel.RegisterModel()
            reg_model.insert_user(data)
            return data.username
        else:
            return "error"


class AddEvent:
    def GET(self):
        return render.Event()


class AllEvents:
    def GET(self):
        x = Events.Events()
        y = x.events_all()
        return render.All_events(y)


class Post_Event:
    def POST(self):
        data = web.input()
        data.username = session_data['user']['username']
        y = Events.Events()
        y.add_event(data)
        return "success"


class CheckLogin:
    def POST(self):
        data = web.input()
        login = LoginModel.LoginModel()
        ans = login.check_user(data)
        if ans == "Incorrect Password" or ans == "User not registered":
            return ans
        else:
            session_data["user"] = ans
            # print(ans)
            # print(session_data["user"])
            return ans


class Logout:
    def GET(self):
        session['user'] = None
        session_data['user'] = None
        session.kill()
        return "success"


if __name__ == '__main__':
    app.run()
