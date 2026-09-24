import QtQuick
import QtQuick.Effects
import ".."

Rectangle {
    id: root

    signal clicked()

    property string text: ""
    property string iconSource: ""
    property int iconSize: 18
    property string variant: "secondary" // "primary", "secondary", "subtle", "danger"
    property bool enabled: true
    property bool tintWithTheme: true

    implicitHeight: 36
    implicitWidth: contentRow.implicitWidth + 24
    radius: FluentTheme.radiusMd

    readonly property bool hovered: mouseArea.containsMouse && root.enabled
    readonly property bool pressed: mouseArea.pressed && root.enabled

    // Color logic based on variant
    color: {
        if (!root.enabled) {
            return FluentTheme.isDark ? "#29161D" : "#E8E8E8"
        }
        if (variant === "primary") {
            if (pressed) return FluentTheme.accentActive
            if (hovered) return FluentTheme.accentHover
            return FluentTheme.accent
        } else if (variant === "danger") {
            if (pressed) return FluentTheme.danger
            if (hovered) return FluentTheme.dangerHover
            return FluentTheme.dangerBg
        } else if (variant === "subtle") {
            if (pressed) return FluentTheme.bgCardActive
            if (hovered) return FluentTheme.bgCardHover
            return "transparent"
        } else {
            // secondary / default
            if (pressed) return FluentTheme.bgCardActive
            if (hovered) return FluentTheme.bgCardHover
            return FluentTheme.bgCard
        }
    }

    border.width: variant === "subtle" ? 0 : 1
    border.color: {
        if (!root.enabled) return "transparent"
        if (variant === "primary") return Qt.rgba(255, 255, 255, 0.15)
        if (variant === "danger") return FluentTheme.danger
        return hovered ? FluentTheme.borderHover : FluentTheme.borderSubtle
    }

    Behavior on color {
        ColorAnimation { duration: FluentTheme.animFast }
    }
    Behavior on border.color {
        ColorAnimation { duration: FluentTheme.animFast }
    }

    Row {
        id: contentRow
        anchors.centerIn: parent
        spacing: 8

        Item {
            id: iconItem
            visible: root.iconSource !== ""
            width: root.iconSize
            height: root.iconSize
            anchors.verticalCenter: parent.verticalCenter

            Image {
                id: rawButtonIcon
                anchors.fill: parent
                source: root.iconSource
                sourceSize.width: root.iconSize
                sourceSize.height: root.iconSize
                visible: !root.tintWithTheme
            }

            MultiEffect {
                anchors.fill: parent
                source: rawButtonIcon
                visible: root.tintWithTheme
                brightness: FluentTheme.isDark ? 0.95 : 0.0
            }
        }

        Text {
            id: label
            visible: root.text !== ""
            text: root.text
            font.family: FluentTheme.fontFamily
            font.pixelSize: FluentTheme.fontSizeBody
            font.weight: variant === "primary" ? Font.DemiBold : Font.Normal
            anchors.verticalCenter: parent.verticalCenter
            color: {
                if (!root.enabled) return FluentTheme.textMuted
                if (variant === "primary") return FluentTheme.accentText
                if (variant === "danger") return FluentTheme.isDark ? "#FF8888" : FluentTheme.danger
                return FluentTheme.textPrimary
            }
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
}
