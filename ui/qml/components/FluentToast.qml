import QtQuick
import ".."

Rectangle {
    id: root

    property string message: ""
    property string type: "info" // "success", "error", "warning", "info"
    property bool showing: false

    width: Math.min(contentRow.implicitWidth + 32, 400)
    height: 44
    radius: FluentTheme.radiusMd

    color: {
        if (type === "success") return FluentTheme.isDark ? "#1C3320" : "#E8F8E8"
        if (type === "error") return FluentTheme.isDark ? "#3A1E20" : "#FDE8E8"
        if (type === "warning") return FluentTheme.isDark ? "#3B331A" : "#FFF8DE"
        return FluentTheme.bgSecondary
    }

    border.width: 1
    border.color: {
        if (type === "success") return FluentTheme.success
        if (type === "error") return FluentTheme.danger
        if (type === "warning") return FluentTheme.warning
        return FluentTheme.borderHover
    }

    opacity: showing ? 1.0 : 0.0
    y: showing ? 0 : -20

    Behavior on opacity {
        NumberAnimation { duration: FluentTheme.animNormal; easing.type: Easing.OutCubic }
    }
    Behavior on y {
        NumberAnimation { duration: FluentTheme.animNormal; easing.type: Easing.OutCubic }
    }

    Row {
        id: contentRow
        anchors.centerIn: parent
        spacing: 10

        Image {
            id: statusIcon
            source: {
                if (root.type === "success") return bridge.icons.check
                if (root.type === "error") return bridge.icons.error
                if (root.type === "warning") return bridge.icons.info
                return bridge.icons.info
            }
            sourceSize.width: 18
            sourceSize.height: 18
            width: 18
            height: 18
            anchors.verticalCenter: parent.verticalCenter
        }

        Text {
            id: msgText
            text: root.message
            font.family: FluentTheme.fontFamily
            font.pixelSize: FluentTheme.fontSizeBody
            color: FluentTheme.textPrimary
            anchors.verticalCenter: parent.verticalCenter
            elide: Text.ElideRight
            maximumLineCount: 1
        }
    }

    Timer {
        id: dismissTimer
        interval: 3500
        running: false
        onTriggered: root.showing = false
    }

    function show(msg, toastType) {
        root.message = msg;
        root.type = toastType || "info";
        root.showing = true;
        dismissTimer.restart();
    }
}
