import QtQuick
import ".."

Rectangle {
    id: root

    property int value: 0 // 0 to 100
    property bool indeterminate: false

    implicitHeight: 6
    implicitWidth: 200
    radius: 3
    color: FluentTheme.isDark ? "#341C26" : "#E5E5E5"
    clip: true

    Rectangle {
        id: fill
        height: parent.height
        radius: 3
        color: FluentTheme.accent
        visible: !root.indeterminate
        width: Math.max(0, Math.min(parent.width, parent.width * (root.value / 100.0)))

        Behavior on width {
            NumberAnimation { duration: FluentTheme.animNormal; easing.type: Easing.OutCubic }
        }
    }

    Rectangle {
        id: indet
        height: parent.height
        radius: 3
        color: FluentTheme.accent
        visible: root.indeterminate
        width: parent.width * 0.35

        SequentialAnimation on x {
            running: root.indeterminate && root.visible
            loops: Animation.Infinite
            NumberAnimation { from: -root.width * 0.35; to: root.width; duration: 1200; easing.type: Easing.InOutQuad }
        }
    }
}
