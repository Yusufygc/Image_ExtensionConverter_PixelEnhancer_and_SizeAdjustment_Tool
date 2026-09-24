import QtQuick
import QtQuick.Controls
import QtQuick.Window
import "."
import "components"
import "views"

ApplicationWindow {
    id: window

    visible: true
    width: 1180
    height: 740
    minimumWidth: 1040
    minimumHeight: 640
    title: bridge ? bridge.strings.appName : "Conventor"
    color: FluentTheme.bgApp

    onClosing: (close) => {
        if (bridge && bridge.isProcessing) {
            bridge.cancelProcessing();
        }
    }

    // Synchronize FluentTheme isDark with bridge
    Binding {
        target: FluentTheme
        property: "isDark"
        value: bridge ? bridge.currentTheme === "dark" : true
    }

    // Ctrl+O shortcut
    Shortcut {
        sequence: "Ctrl+O"
        onActivated: bridge.browseFiles()
    }

    // Window Container
    Item {
        anchors.fill: parent
        anchors.margins: 16

        Column {
            anchors.fill: parent
            spacing: 14

            // Top Header Bar
            Rectangle {
                width: parent.width
                height: 44
                color: "transparent"

                Row {
                    anchors.left: parent.left
                    anchors.verticalCenter: parent.verticalCenter
                    spacing: 10

                    Text {
                        text: bridge.strings.appName
                        font.family: FluentTheme.fontFamily
                        font.pixelSize: FluentTheme.fontSizeTitle
                        font.weight: Font.DemiBold
                        color: FluentTheme.textPrimary
                        anchors.verticalCenter: parent.verticalCenter
                    }
                }

                // Header Action Buttons (Theme Toggle & Info)
                Row {
                    anchors.right: parent.right
                    anchors.verticalCenter: parent.verticalCenter
                    spacing: 6

                    // Theme Toggle Button
                    FluentIconButton {
                        iconSource: FluentTheme.isDark ? bridge.icons.sun : bridge.icons.moon
                        tintWithTheme: false
                        tooltipText: FluentTheme.isDark ? bridge.strings.themeLightTooltip : bridge.strings.themeDarkTooltip
                        buttonSize: 36
                        onClicked: bridge.toggleTheme()
                    }

                    // Info Button
                    FluentIconButton {
                        iconSource: bridge.icons.info
                        tooltipText: bridge.strings.infoTooltip
                        buttonSize: 36
                        onClicked: aboutModal.isOpen = true
                    }
                }
            }

            // Split View Body: Left (Files) & Right (Control Panel)
            Row {
                width: parent.width
                height: parent.height - 58
                spacing: 14

                // Left Panel: Files & DropZone (Expands dynamically to fit 4+ columns)
                FilesPanel {
                    width: parent.width - controlPanel.width - 14
                    height: parent.height
                }

                // Right Panel: Control & Options (Optimal fixed/proportional width)
                ControlPanel {
                    id: controlPanel
                    width: Math.min(410, Math.max(370, Math.round(parent.width * 0.34)))
                    height: parent.height
                }
            }
        }

        // Floating Toast Notification
        FluentToast {
            id: toast
            anchors.top: parent.top
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.topMargin: 20
            z: 9990
        }

        // Info / About Modal
        AboutModal {
            id: aboutModal
            anchors.fill: parent
            z: 9999
        }
    }

    // Connect bridge signals to toast
    Connections {
        target: bridge
        function onToastRequested(msg, toastType) {
            toast.show(msg, toastType);
        }
    }
}
