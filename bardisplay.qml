import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Window 2.0

ApplicationWindow {

    function activate() {

    }

    function setFlow(id, text) {
        if (id == "1") {
            beerFlow1.text = text
        } else {
            beerFlow2.text = text
        }
    }

    function setAmount(id, text) {
        if (id == "1") {
            beerLeft1.text = text
        } else {
            beerLeft2.text = text
        }
    }

    function setTotal(text) {
        totalConsume.text = text
    }

    function setSpotifyText(text) {
        spotifyText.text = text
    }

    function rotateLogo() {
        if (logo.state == "rotated") {
            logo.state = "notrotated"
        } else {
            logo.state = "rotated"
        }
    }

    function setSpotifyCover(image) {
        spotifyCover.source = image
    }

    Component.onCompleted: activate();

    Rectangle {
        id: page
        width: 800; height: 480
        color: "black"

        Image {
            id: logo
            width: 149
            height: 118
            y: 100
            source: "img/logo.png"
            anchors.horizontalCenter: page.horizontalCenter

            states: State {
                name: "rotated"
                PropertyChanges { target: logo; rotation: 180 }
            }

            transitions: Transition {
                RotationAnimation { duration: 1000; direction: RotationAnimation.Counterclockwise }
            }

            MouseArea { anchors.fill: parent; onClicked: rotateLogo() }

        }

        Item {
            id: beerType1
            width: 320
            y: 10
            anchors.left: page.left

            Text {
                id: beerTitle1
                text: "Alsvika IPA"
                color: "white"
                font.pointSize: 24; font.bold: true
                anchors.horizontalCenter: beerType1.horizontalCenter
            }

            Image {
                y: 50
                width: 100
                height: 100
                source: "img/beer-icon.png"
                anchors.horizontalCenter: beerType1.horizontalCenter
            }

            Text {
                id: beerInfo1
                text: "Kraftig IPA fra 6. mars, 7,5% alk."
                color: "white"
                y: 180
                font.pointSize: 10; font.bold: true
                anchors.horizontalCenter: beerType1.horizontalCenter
            }

            Text {
                id: beerFlow1
                text: "1,34 L"
                horizontalAlignment: Text.AlignHCenter
                color: "white"
                y: 220
                font.pointSize: 32; font.bold: true
                anchors.horizontalCenter: beerType1.horizontalCenter
            }

            Text {
                id: beerLeft1
                text: "18,82 L"
                horizontalAlignment: Text.AlignHCenter
                color: "white"
                y: 280
                font.pointSize: 17; font.bold: true
                anchors.horizontalCenter: beerType1.horizontalCenter
            }
        }

        Item {
            id: beerType2
            width: 320
            y: 10
            anchors.right: page.right

            Text {
                id: beerTitle2
                text: "Alsvika Session"
                color: "white"
                font.pointSize: 24; font.bold: true
                anchors.horizontalCenter: beerType2.horizontalCenter
            }

            Image {
                y: 50
                width: 100
                height: 100
                source: "img/beer-icon2.png"
                anchors.horizontalCenter: beerType2.horizontalCenter
            }

            Text {
                id: beerInfo2
                text: "Mildere IPA fra desember, 5% alk."
                color: "white"
                y: 180
                font.pointSize: 10; font.bold: true
                anchors.horizontalCenter: beerType2.horizontalCenter
            }

            Text {
                id: beerFlow2
                text: "2,34 L"
                horizontalAlignment: Text.AlignHCenter
                color: "white"
                y: 220
                font.pointSize: 32; font.bold: true
                anchors.horizontalCenter: beerType2.horizontalCenter
            }

            Text {
                id: beerLeft2
                text: "17,82 L"
                horizontalAlignment: Text.AlignHCenter
                color: "white"
                y: 280
                font.pointSize: 17; font.bold: true
                anchors.horizontalCenter: beerType2.horizontalCenter
            }
        }

        Text {
            id: totalConsume
            text: "Totalt konsumert: 5,2 L"
            horizontalAlignment: Text.AlignHCenter
            color: "white"
            y: 455
            x: 550
            font.pointSize: 13; font.bold: true

        }

        Item {
            id: spotifyMeta
            y: 385
            x: 0

            anchors.horizontalCenter: page.left

            Image {
                id: spotifyCover
                x: 5
                width: 90
                height: 90
                source: ""
            }

            Text {
                id: spotifyText
                x: 100
                font.pointSize: 13
                font.bold: true

                color: "white"
                text: "Spotify - Track"
            }
        }
    }
}
