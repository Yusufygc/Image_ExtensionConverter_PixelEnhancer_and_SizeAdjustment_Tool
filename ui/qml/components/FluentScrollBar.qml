import QtQuick
import QtQuick.Controls.Basic
import ".."

ScrollBar {
    id: control

    implicitWidth: 10
    padding: 1
    hoverEnabled: true
    policy: ScrollBar.AsNeeded

    // Thumb (Pill)
    contentItem: Rectangle {
        implicitWidth: 8
        implicitHeight: 40
        radius: 4
        color: control.pressed
               ? (FluentTheme.isDark ? "#CCCCCC" : "#1A1A1A")
               : (control.hovered
                  ? (FluentTheme.isDark ? "#9E9E9E" : "#4A4A4A")
                  : (FluentTheme.isDark ? "#666666" : "#8A8A8A"))

        opacity: control.size < 1.0 ? 1.0 : 0.0

        Behavior on color {
            ColorAnimation { duration: FluentTheme.animFast }
        }
        Behavior on opacity {
            NumberAnimation { duration: FluentTheme.animFast }
        }
    }

    // Track
    background: Rectangle {
        implicitWidth: 10
        radius: 5
        color: FluentTheme.isDark ? "#29161D" : "#EAEAEA"
        border.color: FluentTheme.isDark ? "#3A2028" : "#DADADA"
        border.width: 1
        opacity: control.size < 1.0 ? (control.hovered || control.pressed ? 0.9 : 0.6) : 0.0

        Behavior on opacity {
            NumberAnimation { duration: FluentTheme.animFast }
        }
    }
}
