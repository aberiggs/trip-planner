import { type ComponentProps } from "react"
import Ionicons from "@expo/vector-icons/Ionicons"
import { type IconProps } from "@expo/vector-icons/build/createIconSet"

import { useThemeColor } from "@/hooks/useThemeColor"
import { ColorTypes } from "@/constants/Colors"

export type ThemedIconProps = IconProps<
  ComponentProps<typeof Ionicons>["name"]
> & {
  lightColor?: string
  darkColor?: string
  color?: ColorTypes
}

export function ThemedIcon({
  style,
  size = 28,
  color = ColorTypes.primary,
  lightColor,
  darkColor,
  ...rest
}: ThemedIconProps) {
  const iconColor = useThemeColor({ light: lightColor, dark: darkColor }, color)
  return (
    <Ionicons size={size} color={iconColor} style={[{}, style]} {...rest} />
  )
}
