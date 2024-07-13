import React from "react"

import { StyleSheet } from "react-native"
import { ThemedView } from "@/components/ThemedView"
import { ThemedText } from "@/components/ThemedText"
import { ThemedButton } from "@/components/ThemedButton"
import { ThemedIcon } from "@/components/ThemedIcon"
import { Colors } from "@/constants/Colors"
import { ColorTypes } from "@/constants/Colors"
import { Link } from "expo-router"
import { ThemedInput } from "@/components/ThemedInput"
import { ThemedBoxShadow } from "@/components/ThemedBoxShadow"

export default function Login() {
  return (
    <>
      <ThemedView style={styles.mainContainer}>
        <ThemedView style={styles.contentContainer}>
          <ThemedText style={styles.title} type="title">
            Welcome back!{"\n"}Time to plan some fun.
          </ThemedText>
          <ThemedView
            style={{
              gap: 30,
              alignItems: "center",
            }}
          >
            <ThemedBoxShadow
              lightShadowColor={Colors.light.primary}
              darkShadowColor={Colors.transparent}
            >
              <ThemedInput
                placeholder="Enter your email"
                keyboardType="email-address"
              />
            </ThemedBoxShadow>
            <ThemedView>
              <ThemedBoxShadow
                lightShadowColor={Colors.light.primary}
                darkShadowColor={Colors.transparent}
              >
                <ThemedInput
                  placeholder="Enter your password"
                  secureTextEntry={true}
                />
              </ThemedBoxShadow>
              <ThemedView style={styles.forgotPasswordContainer}>
                <Link href="/forgot-password" asChild>
                  <ThemedText color={ColorTypes.secondary}>
                    Forgot Password?
                  </ThemedText>
                </Link>
              </ThemedView>
            </ThemedView>
            <ThemedBoxShadow>
              <Link replace style={[styles.loginButton]} href="" asChild>
                <ThemedButton color={ColorTypes.primary}>
                  <ThemedText color={ColorTypes.base}>Log in</ThemedText>
                </ThemedButton>
              </Link>
            </ThemedBoxShadow>
          </ThemedView>
          <ThemedView style={styles.separatorContainer}>
            <ThemedView style={styles.separatorLine} />
            <ThemedText style={styles.separatorText} color={ColorTypes.primary}>
              or continue with
            </ThemedText>
            <ThemedView style={styles.separatorLine} />
          </ThemedView>
          <ThemedBoxShadow>
            <Link
              replace
              style={[styles.googleButton]}
              href="google-login"
              asChild
            >
              <ThemedButton color={ColorTypes.base}>
                <ThemedIcon color={ColorTypes.primary} name="logo-google" />
                <ThemedText color={ColorTypes.primary}>Google</ThemedText>
              </ThemedButton>
            </Link>
          </ThemedBoxShadow>
        </ThemedView>
        <ThemedView style={styles.footerContainer}>
          <ThemedText>
            No account? Register
            <Link href="" replace asChild>
              <ThemedText style={{ fontWeight: "bold" }}> here</ThemedText>
            </Link>
          </ThemedText>
        </ThemedView>
      </ThemedView>
    </>
  )
}

const styles = StyleSheet.create({
  mainContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  contentContainer: {
    flexDirection: "column",
    justifyContent: "space-between",
    alignItems: "center",
  },
  title: {
    marginBottom: 40,
    lineHeight: 45,
  },
  loginButton: {
    width: 300,
    height: 45,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-around",
  },
  forgotPasswordContainer: {
    marginTop: 10,
    width: 300,
    alignItems: "flex-end",
  },
  separatorContainer: {
    width: 300,
    flexDirection: "row",
    alignItems: "center",
    marginVertical: 20,
  },
  separatorLine: {
    flex: 1,
    height: 1,
    backgroundColor: Colors.light.secondary,
  },
  separatorText: {
    marginHorizontal: 10,
  },
  googleButton: {
    width: 300,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 10,
  },
  footerContainer: {
    position: "absolute",
    bottom: 45,
    width: "100%",
    alignItems: "center",
  },
})
