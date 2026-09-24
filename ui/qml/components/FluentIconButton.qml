import QtQuick
import QtQuick.Effects
import ".."

Rectangle {
    id: root

    signal clicked()

    property string iconSource: ""
    property string tooltipText: ""
    property int iconSize: 18
    property int buttonSize: 34
    property bool active: false
    property bool enabled: true
    property bool tintWithTheme: true

    width: buttonSize
    height: buttonSize
    radius: FluentTheme.radiusMd

    readonly property bool hovered: mouseArea.containsMouse && root.enabled
    readonly property bool pressed: mouseArea.pressed && root.enabled

    color: {
        if (!root.enabled) return "transparent"
        if (active) return FluentTheme.isDark ? "#4E2C39" : "#E2E2E2"
        if (pressed) return FluentTheme.bgCardActive
        if (hovered) return FluentTheme.bgCardHover
        return "transparent"
    }

    border.width: active ? 1 : 0
    border.color: active ? FluentTheme.borderHover : "transparent"

    Behavior on color {
        ColorAnimation { duration: FluentTheme.animFast }
    }

    Item {
        id: iconWrapper
        width: root.iconSize
        height: root.iconSize
        anchors.centerIn: parent

        Image {
            id: rawIcon
            anchors.fill: parent
            source: root.iconSource
            sourceSize.width: root.iconSize
            sourceSize.height: root.iconSize
            visible: !root.tintWithTheme
            opacity: root.enabled ? (root.active ? 1.0 : (root.hovered ? 1.0 : 0.8)) : 0.4
        }

        MultiEffect {
            anchors.fill: parent
            source: rawIcon
            visible: root.tintWithTheme
            brightness: FluentTheme.isDark ? 0.95 : 0.0
            opacity: root.enabled ? (root.active ? 1.0 : (root.hovered ? 1.0 : 0.8)) : 0.4
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: root.enabled
        cursorShape: root.enabled ? Qt.PointingHandCursor : Qt.ArrowCursor
        onClicked: {
            if (root.enabled) root.clicked()
        }
    }

    // Windows 11 style clamped Tooltip in Window overlay layer (no clipping, always on top)
    Loader {
        active: mouseArea.containsMouse && root.tooltipText !== "" && root.Window.contentItem !== null
        sourceComponent: Component {
            Item {
                parent: root.Window.contentItem
                z: 99999

                property var pt: root.mapToItem(root.Window.contentItem, 0, 0)
                property real tipWidth: tipLabel.implicitWidth + 18

                Rectangle {
                    x: Math.max(8, Math.min(root.Window.contentItem.width - tipWidth - 8, pt.x + (root.width - tipWidth) / 2))
                    y: pt.y + root.height + 6
                    width: tipWidth
                    height: 26
                    radius: FluentTheme.radiusSm
                    color: FluentTheme.isDark ? "#2D2D2D" : "#323130"
                    border.color: FluentTheme.isDark ? "#454545" : "#505050"
                    border.width: 1

                    Text {
                        id: tipLabel
                        text: root.tooltipText
                        anchors.centerIn: parent
                        color: "#FFFFFF"
                        font.family: FluentTheme.fontFamily
                        font.pixelSize: FluentTheme.fontSizeSmall
                    }
                }
            }
        }
    }
}
