import QtQuick
import ".."

Rectangle {
    id: root

    signal valueModified(var val)

    property real value: 100
    property real from: 1
    property real to: 10000
    property real stepSize: 1
    property string suffix: ""
    property int decimals: 0

    implicitHeight: 36
    implicitWidth: 140
    radius: FluentTheme.radiusMd
    color: FluentTheme.bgInput
    border.color: FluentTheme.borderSubtle
    border.width: 1

    Behavior on border.color {
        ColorAnimation { duration: FluentTheme.animFast }
    }

    TextInput {
        id: textInput
        anchors.left: parent.left
        anchors.leftMargin: 12
        anchors.right: stepperColumn.left
        anchors.rightMargin: 6
        anchors.verticalCenter: parent.verticalCenter
        color: FluentTheme.textPrimary
        font.family: FluentTheme.fontFamily
        font.pixelSize: FluentTheme.fontSizeBody
        text: root.decimals > 0 ? root.value.toFixed(root.decimals) + root.suffix : Math.round(root.value) + root.suffix
        selectByMouse: true

        onEditingFinished: {
            var cleanText = text.replace(root.suffix, "").trim();
            var parsed = parseFloat(cleanText);
            if (!isNaN(parsed)) {
                var clamped = Math.max(root.from, Math.min(root.to, parsed));
                root.value = clamped;
                root.valueModified(clamped);
            }
            text = root.decimals > 0 ? root.value.toFixed(root.decimals) + root.suffix : Math.round(root.value) + root.suffix;
        }

        onActiveFocusChanged: {
            root.border.color = activeFocus ? FluentTheme.accent : FluentTheme.borderSubtle;
        }
    }

    Column {
        id: stepperColumn
        anchors.right: parent.right
        anchors.rightMargin: 5
        anchors.verticalCenter: parent.verticalCenter
        width: 26
        height: 29
        spacing: 1

        // Up Stepper Arrow (kutusuz)
        Item {
            width: 26
            height: 14

            Canvas {
                id: upChevron
                width: 12
                height: 7
                anchors.centerIn: parent
                antialiasing: true
                opacity: upMouse.containsMouse ? 1.0 : 0.75
                onPaint: {
                    var ctx = getContext("2d");
                    ctx.reset();
                    ctx.beginPath();
                    ctx.moveTo(1.5, 5.5);
                    ctx.lineTo(6, 1.5);
                    ctx.lineTo(10.5, 5.5);
                    ctx.lineWidth = 2.4;
                    ctx.strokeStyle = FluentTheme.accent;
                    ctx.lineCap = "round";
                    ctx.lineJoin = "round";
                    ctx.stroke();
                }

                Connections {
                    target: FluentTheme
                    function onIsDarkChanged() { upChevron.requestPaint(); }
                }
            }

            MouseArea {
                id: upMouse
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: {
                    var newVal = Math.min(root.to, root.value + root.stepSize);
                    root.value = newVal;
                    root.valueModified(newVal);
                }
            }
        }

        // Down Stepper Arrow (kutusuz)
        Item {
            width: 26
            height: 14

            Canvas {
                id: downChevron
                width: 12
                height: 7
                anchors.centerIn: parent
                antialiasing: true
                opacity: downMouse.containsMouse ? 1.0 : 0.75
                onPaint: {
                    var ctx = getContext("2d");
                    ctx.reset();
                    ctx.beginPath();
                    ctx.moveTo(1.5, 1.5);
                    ctx.lineTo(6, 5.5);
                    ctx.lineTo(10.5, 1.5);
                    ctx.lineWidth = 2.4;
                    ctx.strokeStyle = FluentTheme.accent;
                    ctx.lineCap = "round";
                    ctx.lineJoin = "round";
                    ctx.stroke();
                }

                Connections {
                    target: FluentTheme
                    function onIsDarkChanged() { downChevron.requestPaint(); }
                }
            }

            MouseArea {
                id: downMouse
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: {
                    var newVal = Math.max(root.from, root.value - root.stepSize);
                    root.value = newVal;
                    root.valueModified(newVal);
                }
            }
        }
    }
}
