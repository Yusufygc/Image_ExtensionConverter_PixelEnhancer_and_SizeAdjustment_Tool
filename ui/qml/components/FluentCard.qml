import QtQuick
import ".."

Rectangle {
    id: root
    property real cornerRadius: FluentTheme.radiusMd
    property color customBg: "transparent"
    property color customBorder: "transparent"
    property bool hoverable: false
    property bool hovered: hoverable && mouseArea.containsMouse

    radius: cornerRadius
    color: customBg !== "transparent" 
           ? customBg 
           : (hovered ? FluentTheme.bgCardHover : FluentTheme.bgCard)

    border.color: customBorder !== "transparent"
                 ? customBorder
                 : (hovered ? FluentTheme.borderHover : FluentTheme.borderCard)
    border.width: 1

    Behavior on color {
        ColorAnimation { duration: FluentTheme.animFast }
    }
    Behavior on border.color {
        ColorAnimation { duration: FluentTheme.animFast }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        enabled: root.hoverable
        hoverEnabled: root.hoverable
    }
}
