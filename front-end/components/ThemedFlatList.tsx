import { FlatList, type FlatListProps } from "react-native"
import { ColorTypes, useThemeColor } from "@/hooks/useThemeColor"

export type ThemedFlatListProps = FlatListProps<any> & {
  lightColor?: string
  darkColor?: string
  color?: ColorTypes
}

export function ThemedFlatList({
  style,
  lightColor,
  darkColor,
  color = ColorTypes.base,
  data,
  ...otherProps
}: ThemedFlatListProps) {
  const backgroundColor = useThemeColor(
    { light: lightColor, dark: darkColor },
    color
  )

  return (
    <FlatList
      style={[{ backgroundColor }, style]}
      data={data}
      {...otherProps}
    />
  )
}
