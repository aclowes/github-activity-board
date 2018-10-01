# GitHub Activity Board

See the recent pull requests and comments from your team.

Getting started: 

    export GITHUB_TOKEN=
    export GITHUB_ORGANIZATION=
    python github_report.py
    
    yarn install
    yarn start

View some example reports for these organizations on the interwebs:

* [Django](http://static.yawn.live/github-activity-board/django/)
* [Kubernetes](http://static.yawn.live/github-activity-board/kubernetes/)

The reports are built weekly using [YAWN]. You can view the build
status in the demo [YAWN instance].

[YAWN]: https://pypi.org/project/yawns
[YAWN instance]: https://yawn.live/workflows/13

The kubernetes report looks like this, for example:

![Kubernetes report screenshot](https://user-images.githubusercontent.com/910316/40887627-6af78422-6700-11e8-80b1-e9c62bf5c8b5.png)

To use standalone:

    export PUBLIC_URL=/$GITHUB_ORGANIZATION
    yarn build
    mv build/ $GITHUB_ORGANIZATION
    python3 -m http.server 8000
