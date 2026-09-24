import QtQuick

pragma Singleton

QtObject {
    id: theme

    // Set by Main.qml according to bridge.currentTheme
    property bool isDark: true

    // Typography
    readonly property string fontFamily: "Segoe UI Variable Display, Segoe UI, sans-serif"
    readonly property int fontSizeSmall: 11
    readonly property int fontSizeBody: 13
    readonly property int fontSizeSubhead: 14
    readonly property int fontSizeTitle: 18
    readonly property int fontSizeHeader: 22

    // Radiuses
    readonly property real radiusSm: 4
    readonly property real radiusMd: 8
    readonly property real radiusLg: 12
    readonly property real radiusXl: 16

    // Animation Durations
    readonly property int animFast: 150
    readonly property int animNormal: 250

    // Dynamic Colors based on isDark
    // Dark mod paleti: "Snack at Midnight" (Mulberry Night / Champagne Silk / Indigo Tart / Glace Apricot / Crushed Cacao)
    // Light mod paleti: "Aqua Nebula" (Midnight Abyss / Atlantic Steel / Tidepool Teal / Summer Surf / Glacier Mist)
    readonly property color bgApp: isDark ? "#0F0807" : "#DEF2FF"
    readonly property color bgSecondary: isDark ? "#29161D" : "#FFFFFF"
    readonly property color bgCard: isDark ? "#432430" : "#FFFFFF"
    readonly property color bgCardHover: isDark ? "#4E2C39" : "#EAF6FF"
    readonly property color bgCardActive: isDark ? "#341C26" : "#D8EEFB"
    readonly property color bgInput: isDark ? "#1C0F13" : "#FFFFFF"

    readonly property color borderSubtle: isDark ? "#3A2028" : "#CFE6F2"
    readonly property color borderCard: isDark ? "#43242E" : "#C7E4F5"
    readonly property color borderHover: isDark ? "#5C3542" : "#2FA0C6"

    readonly property color textPrimary: isDark ? "#CEB3AB" : "#061826"
    readonly property color textSecondary: isDark ? "#A6897F" : "#1C4E75"
    readonly property color textMuted: isDark ? "#7D645C" : "#5E85A3"

    readonly property color accent: isDark ? "#E8AC97" : "#2FA0C6"
    readonly property color accentHover: isDark ? "#F0C0AE" : "#58C9F3"
    readonly property color accentActive: isDark ? "#D89A82" : "#227E9C"
    readonly property color accentText: isDark ? "#2A1418" : "#FFFFFF"
    readonly property color tabActiveBg: isDark ? "#2A3548" : "#BDE5FF"
    
    readonly property color danger: isDark ? "#FF5555" : "#C42B1C"
    readonly property color dangerHover: isDark ? "#FF6E6E" : "#D1382A"
    readonly property color dangerBg: isDark ? "#381E20" : "#FDE7E9"
    
    readonly property color success: isDark ? "#6CCB5F" : "#0F7B0F"
    readonly property color successBg: isDark ? "#1C3320" : "#DFF6DD"
    
    readonly property color warning: isDark ? "#FCE100" : "#9D5D00"
    readonly property color warningBg: isDark ? "#3B331A" : "#FFF4CE"
}
