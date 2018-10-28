import QtQuick 2.10
import QtQuick.Controls 2.1
import QtQuick.Window 2.2
import QtQuick.Controls.Material 2.3

ApplicationWindow {
    id: applicationWindow
    title: qsTr("Spring Terminal")
    visible: true

    width: 800
    height: 600
    color: "#565656"
    opacity: 1

    Rectangle  {

        x: 25
        y: 107
        width: 759
        height: 419

        color: "#bf000000"
        radius: 13
        border.width: 3

        TextEdit {

            id: textEdit
            x: 8
            y: 8
            width: 743
            height: 403
            color: "#f8a119"
            text: qsTr("Text Edit")
            cursorVisible: false
            font.capitalization: Font.AllUppercase
            font.bold: true
            readOnly: true
            clip: false
            font.family: "Courier"
            font.pixelSize: 16
        }
    }

    Rectangle {
        x: 25
        y: 538
        width: 759
        height: 52
        color: "#bf000000"
        radius: 13
        border.width: 3

        TextInput {
            id: textInput
            x: 13
            y: 8
            width: 733
            height: 36
            color: "#f8a119"
            text: qsTr("Text Input")
            cursorVisible: true
            font.weight: Font.Bold
            font.capitalization: Font.AllUppercase
            font.family: "Courier"
            font.pixelSize: 16
            onAccepted: Manager.prompt = text
        }
    }

    Switch {
        id: switch1
        x: 600
        y: 56
        width: 142
        height: 30
        text: qsTr("Connect")
        onPositionChanged: Manager.connection = position
    }
}
