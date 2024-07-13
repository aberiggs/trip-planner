import {
  Pressable,
  type PressableProps,
  ViewStyle,
  PressableStateCallbackType,
  StyleProp,
} from "react-native"
import { useCallback, forwardRef } from "react"
import { ColorTypes, useThemeColor } from "@/hooks/useThemeColor"

export type ThemedPressableProps = PressableProps & {
  forwardedRef?: any // For case where a <Link /> component wraps this
  lightColor?: string
  darkColor?: string
  color?: ColorTypes
}

// Imp = Implementation
function ThemedButtonImp({
  forwardedRef,
  style,
  lightColor,
  darkColor,
  color = ColorTypes.primary,
  ...otherProps
}: ThemedPressableProps) {
  const backgroundColor = useThemeColor(
    { light: lightColor, dark: darkColor },
    color
  )

  // style is either a ViewStyle or a function that returns a ViewStyle :)
  const getStyle = useCallback(
    (state: PressableStateCallbackType): StyleProp<ViewStyle> => {
      const incomingStyle = typeof style === "function" ? style(state) : style
      return [
        { borderRadius: 5, padding: 10, margin: 10 },
        { backgroundColor, opacity: state.pressed ? 0.8 : 1 },
        incomingStyle,
      ]
    },
    [style, backgroundColor]
  )

  // Return a pressable with the set background color and text color
  return <Pressable ref={forwardedRef} style={getStyle} {...otherProps} />
}

// Wrapping with a forwardRef so that the ref can be passed to the Pressable.
export const ThemedButton = forwardRef<
  typeof ThemedButtonImp,
  ThemedPressableProps
>(function ThemedButton(props, ref) {
  return <ThemedButtonImp {...props} forwardedRef={ref} />
})
