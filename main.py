import argparse
import json
from http.client import HTTPSConnection


def get_events(username: str):
    conn = HTTPSConnection("api.github.com")
    headers = {"User-Agent": "Python script to get info about user events"}
    conn.request("GET", f"/users/{username}/events", headers=headers)
    response = conn.getresponse()
    print(response.status)
    if response.status == 304:
        print("Not modified")
    elif response.status == 403:
        print("Forbidden")
    elif response.status == 503:
        print("Service unavailable")
    elif response.status == 404:
        print("Username is incorrect")
    else:
        data = response.read()
        # with open("response.json", "wb") as f:
        # f.write(data)
        data_json = json.loads(data)
        for info in data_json:
            action = info["type"]
            match action:
                case "IssueCommentEvent":
                    act = "commented on"
                case "PullRequestEvent":
                    act = "pulled"
                case "PushEvent":
                    act = "pushed"
                case "IssuesEvent":
                    act = "created an issue in"
                case "WatchEvent":
                    act = "started watching"
                case _:
                    act = action
            name = info["repo"]["name"]
            date = info["created_at"][5:10]
            print(f"On {date} {act} {name}")


def main():
    parser = argparse.ArgumentParser(
        description="Get public events using Github Api"
    )
    parser.add_argument(
        "username", type=str, help="Username to fetch github events"
    )
    args = parser.parse_args()
    get_events(args.username)


if __name__ == "__main__":
    main()
