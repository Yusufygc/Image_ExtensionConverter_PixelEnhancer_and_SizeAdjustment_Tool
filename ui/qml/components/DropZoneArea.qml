import QtQuick
import ".."

Rectangle {
    id: root

    property bool isDragOver: dropArea.containsDrag

    radius: FluentTheme.radiusLg
    color: isDragOver ? (FluentTheme.isDark ? "#2A3644" : "#EAF4FD") : (mouseArea.containsMouse ? FluentTheme.bgCardHover : FluentTheme.bgCard)
    border.color: isDragOver ? FluentTheme.accent : (mouseArea.containsMouse ? FluentTheme.borderHover : FluentTheme.borderSubtle)
    border.width: isDragOver ? 2 : 1

    Behavior on color {
        ColorAnimation { duration: FluentTheme.animFast }
    }
    Behavior on border.color {
        ColorAnimation { duration: FluentTheme.animFast }
    }

    Column {
        anchors.centerIn: parent
        spacing: 12

        Rectangle {
            width: 56
            height: 56
            radius: 28
            color: root.isDragOver ? FluentTheme.accent : (FluentTheme.isDark ? "#353535" : "#EBEBEB")
            anchors.horizontalCenter: parent.horizontalCenter

            Behavior on color {
                ColorAnimation { duration: FluentTheme.animFast }
            }

            Image {
                source: bridge.icons.upload
                sourceSize.width: 28
                sourceSize.height: 28
                width: 28
                height: 28
                anchors.centerIn: parent
                opacity: 0.9
            }
        }

        Text {
            text: root.isDragOver ? bridge.strings.dropActive : bridge.strings.dropTitle
            font.family: FluentTheme.fontFamily
            font.pixelSize: FluentTheme.fontSizeSubhead
            font.weight: Font.DemiBold
            color: root.isDragOver ? FluentTheme.accent : FluentTheme.textPrimary
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            text: bridge.strings.dropSub
            font.family: FluentTheme.fontFamily
            font.pixelSize: FluentTheme.fontSizeSmall
            color: FluentTheme.textSecondary
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }

    DropArea {
        id: dropArea
        anchors.fill: parent
        keys: ["text/uri-list"]

        onDropped: (drop) => {
            if (drop.hasUrls) {
                var urls = [];
                for (var i = 0; i < drop.urls.length; i++) {
                    urls.push(drop.urls[i]);
                }
                bridge.addFiles(urls);
                drop.acceptProposedAction();
            }
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
        onClicked: {
            bridge.browseFiles();
        }
    }
}
