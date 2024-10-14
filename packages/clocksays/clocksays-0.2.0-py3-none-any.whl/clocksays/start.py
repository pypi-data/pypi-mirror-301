import clocksays.saytime as st
import datetime as dt


def test():
    for m in range(60):
        t = dt.datetime.strptime(f"2024-01-01 14:{m:02}:01", "%Y-%m-%d %H:%M:%S")
        print(t, st.clocksays(t=t, language="de", prefix='Es ist ', suffix='.'))
        print(t, st.clocksays(t=t, language="en", prefix='It is ', suffix='.'))
        print(t, st.clocksays(t=t, language="fr", prefix='Il est ', suffix='.'))
    # for m in range(60):
    #     t = dt.datetime.strptime(f"2024-01-01 14:{m:02}:01", "%Y-%m-%d %H:%M:%S")
    #     print(t, st.clocksays(t=t, language="en", prefix='It is ', suffix='.'))


def test2():
    t = dt.datetime.strptime("2024-01-01 14:01:01", "%Y-%m-%d %H:%M:%S")
    print(t, st.time2words(t=t))
    t = dt.datetime.strptime("2024-01-01 11:16:01", "%Y-%m-%d %H:%M:%S")
    print(t, st.time2words(t=t))
    t = dt.datetime.strptime("2024-01-01 11:32:01", "%Y-%m-%d %H:%M:%S")
    print(t, st.time2words(t=t))
    t = dt.datetime.strptime("2024-01-01 11:46:01", "%Y-%m-%d %H:%M:%S")
    print(t, st.time2words(t=t))
    t = dt.datetime.strptime("2024-01-01 13:58:01", "%Y-%m-%d %H:%M:%S")
    print(t, st.time2words(t=t))
    t = dt.datetime.strptime("2024-01-01 23:14:01", "%Y-%m-%d %H:%M:%S")
    print(t, st.time2words(t=t))
    t = dt.datetime.strptime("2024-01-01 09:28:01", "%Y-%m-%d %H:%M:%S")
    print(t, st.time2words(t=t))
    t = dt.datetime.strptime("2024-01-01 02:44:01", "%Y-%m-%d %H:%M:%S")
    print(t, st.time2words(t=t))
    t = dt.datetime.strptime("2024-01-01 23:15:01", "%Y-%m-%d %H:%M:%S")
    print(t, st.time2words(t=t))
    t = dt.datetime.strptime("2024-01-01 09:30:01", "%Y-%m-%d %H:%M:%S")
    print(t, st.time2words(t=t))
    t = dt.datetime.strptime("2024-01-01 02:00:01", "%Y-%m-%d %H:%M:%S")
    print(t, st.time2words(t=t))
    t = dt.datetime.strptime("2024-01-01 07:45:01", "%Y-%m-%d %H:%M:%S")
    print(t, st.time2words(t=t))

    t = dt.datetime.strptime("2024-01-01 07:12:01", "%Y-%m-%d %H:%M:%S")
    print(t, st.time2words(t=t))
    t = dt.datetime.strptime("2024-01-01 07:20:01", "%Y-%m-%d %H:%M:%S")
    print(t, st.time2words(t=t))

    t = dt.datetime.strptime("2024-01-01 07:33:01", "%Y-%m-%d %H:%M:%S")
    print(t, st.time2words(t=t))
    t = dt.datetime.strptime("2024-01-01 09:38:01", "%Y-%m-%d %H:%M:%S")
    print(t, st.time2words(t=t))

    t = dt.datetime.strptime("2024-01-01 07:20:01", "%Y-%m-%d %H:%M:%S")
    print(t, st.time2words(t=t))

    t = dt.datetime.strptime("2024-01-01 07:21:01", "%Y-%m-%d %H:%M:%S")
    print(t, st.time2words(t=t))

    t = dt.datetime.strptime("2024-01-01 09:48:01", "%Y-%m-%d %H:%M:%S")
    print(t, st.time2words(t=t))
    t = dt.datetime.strptime("2024-01-01 09:52:01", "%Y-%m-%d %H:%M:%S")
    print(t, st.time2words(t=t))


def main():
    pass


if __name__ == "__main__":
    main()
