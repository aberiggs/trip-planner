import { View, type ViewProps } from "react-native"

import { useThemeColor, ColorTypes } from "@/hooks/useThemeColor"

export type ThemedViewProps = ViewProps & {
  lightColor?: string
  darkColor?: string
  color?: ColorTypes
}

export function ThemedView({
  style,
  lightColor,
  darkColor,
  color = ColorTypes.base,
  ...otherProps
}: ThemedViewProps) {
  const backgroundColor = useThemeColor(
    { light: lightColor, dark: darkColor },
    color
  )

  return <View style={[{ backgroundColor }, style]} {...otherProps} />
}
