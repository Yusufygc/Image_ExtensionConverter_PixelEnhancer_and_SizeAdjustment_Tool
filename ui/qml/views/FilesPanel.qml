import QtQuick
import QtQuick.Controls
import ".."
import "../components"

Rectangle {
    id: root

    color: FluentTheme.bgSecondary
    border.color: FluentTheme.borderSubtle
    border.width: 1
    radius: FluentTheme.radiusLg

    Column {
        anchors.fill: parent
        anchors.margins: 14
        spacing: 12

        // Top Toolbar
        Item {
            width: parent.width
            height: 38

            Row {
                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
                spacing: 8

                // Add Files Button
                FluentButton {
                    text: "Dosya Ekle"
                    iconSource: bridge.icons.upload
                    variant: "secondary"
                    implicitHeight: 34
                    anchors.verticalCenter: parent.verticalCenter
                    onClicked: bridge.browseFiles()
                }

                // View Mode Toggle (Grid vs List)
                Row {
                    anchors.verticalCenter: parent.verticalCenter
                    spacing: 2

                    FluentIconButton {
                        iconSource: bridge.icons.grid
                        tooltipText: bridge.strings.tooltipGrid
                        active: bridge.viewMode === "grid"
                        buttonSize: 34
                        onClicked: bridge.setViewMode("grid")
                    }

                    FluentIconButton {
                        iconSource: bridge.icons.list
                        tooltipText: bridge.strings.tooltipList
                        active: bridge.viewMode === "list"
                        buttonSize: 34
                        onClicked: bridge.setViewMode("list")
                    }
                }

                // Sort Dropdown
                FluentComboBox {
                    id: sortCombo
                    anchors.verticalCenter: parent.verticalCenter
                    implicitHeight: 34
                    implicitWidth: 160
                    model: [
                        bridge.strings.sortNameAsc,
                        bridge.strings.sortNameDesc,
                        bridge.strings.sortSizeAsc,
                        bridge.strings.sortSizeDesc,
                        bridge.strings.sortStatus
                    ]
                    currentIndex: 0
                    onActivated: (index) => {
                        var options = ["name_asc", "name_desc", "size_asc", "size_desc", "status"];
                        bridge.sortFiles(options[index]);
                    }
                }
            }

            Row {
                anchors.right: parent.right
                anchors.verticalCenter: parent.verticalCenter
                spacing: 8

                // Delete Selected Button (Active when items selected)
                FluentButton {
                    text: bridge.strings.deleteSelected
                    iconSource: bridge.icons.delete
                    variant: "danger"
                    visible: bridge.selectedCount > 0
                    enabled: bridge.selectedCount > 0
                    implicitHeight: 34
                    anchors.verticalCenter: parent.verticalCenter
                    onClicked: bridge.removeSelectedFiles()
                }

                // Clear All Button
                FluentButton {
                    text: bridge.strings.clearAll
                    iconSource: bridge.icons.trash
                    variant: "subtle"
                    visible: bridge.totalCount > 0
                    implicitHeight: 34
                    anchors.verticalCenter: parent.verticalCenter
                    onClicked: bridge.clearFiles()
                }
            }
        }

        // Info / Count Header Bar
        Rectangle {
            width: parent.width
            height: 28
            color: "transparent"

            Row {
                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
                spacing: 8

                Text {
                    text: bridge.totalCount > 0 ? (bridge.totalCount + " dosya") : "Henüz dosya eklenmedi"
                    font.family: FluentTheme.fontFamily
                    font.pixelSize: FluentTheme.fontSizeSmall
                    font.weight: Font.DemiBold
                    color: FluentTheme.textSecondary
                }

                Text {
                    visible: bridge.selectedCount > 0
                    text: "(" + bridge.selectedCount + " seçili)"
                    font.family: FluentTheme.fontFamily
                    font.pixelSize: FluentTheme.fontSizeSmall
                    color: FluentTheme.accent
                }
            }

            // Select all / Deselect toggle button
            Text {
                visible: bridge.totalCount > 0
                anchors.right: parent.right
                anchors.verticalCenter: parent.verticalCenter
                text: bridge.selectedCount === bridge.totalCount ? "Seçimi Kaldır" : bridge.strings.selectAll
                font.family: FluentTheme.fontFamily
                font.pixelSize: FluentTheme.fontSizeSmall
                color: FluentTheme.accent

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        bridge.selectAllFiles(bridge.selectedCount !== bridge.totalCount);
                    }
                }
            }
        }

        // Main Content Area: DropZone or File Grid/List
        Item {
            width: parent.width
            height: parent.height - 86
            clip: true

            // Empty state: Full DropZone
            DropZoneArea {
                anchors.fill: parent
                visible: bridge.totalCount === 0
            }

            // Grid View (Dinamik 4 sütun + Modern Windows 11 Fluent ScrollBar)
            GridView {
                id: gridView
                anchors.fill: parent
                visible: bridge.totalCount > 0 && bridge.viewMode === "grid"
                clip: true
                boundsBehavior: Flickable.StopAtBounds

                // Dinamik sütun hesabı: Varsayılan pencere boyutunda tam 4 sütun garanti edilir.
                // Scrollbar için 14px ayrılır ve kalan alan 4 sütuna dengeli dağıtılır.
                readonly property int columns: Math.max(1, Math.floor((width - 14) / 148))
                cellWidth: Math.floor((width - 14) / columns)
                cellHeight: 176

                model: bridge.fileList
                delegate: Item {
                    width: gridView.cellWidth
                    height: gridView.cellHeight

                    FileCardItem {
                        anchors.centerIn: parent
                        itemData: modelData
                    }
                }

                ScrollBar.vertical: FluentScrollBar {
                    id: gridScrollBar
                }
            }

            // List View (Modern Windows 11 Fluent ScrollBar)
            ListView {
                id: listView
                anchors.fill: parent
                visible: bridge.totalCount > 0 && bridge.viewMode === "list"
                spacing: 6
                clip: true
                boundsBehavior: Flickable.StopAtBounds
                model: bridge.fileList
                delegate: Item {
                    width: listView.width - 14
                    height: 48

                    FileListItem {
                        anchors.fill: parent
                        itemData: modelData
                    }
                }

                ScrollBar.vertical: FluentScrollBar {
                    id: listScrollBar
                }
            }

            // Drop Area on top of populated list to allow dropping more files anytime
            DropArea {
                id: popDropArea
                anchors.fill: parent
                enabled: bridge.totalCount > 0
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

            // Subtle drop highlight border when dragging over populated list
            Rectangle {
                anchors.fill: parent
                radius: FluentTheme.radiusMd
                color: Qt.rgba(0, 0.4, 0.8, 0.08)
                border.color: FluentTheme.accent
                border.width: 2
                visible: popDropArea.containsDrag
            }
        }
    }
}
