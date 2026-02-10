# Hello World and Composable Previews in Android Studio

I've been using Android phones for several years now, and it has always been on my bucket list to write myself some productivity apps. This morning I thought I'd get reacquainted with Android app development.

The official Android developer documentation site has an excellent Hello World tutorial: <https://developer.android.com/codelabs/basic-android-kotlin-compose-first-app>

Following the tutorial, I was up and coding within minutes. Kotlin made the code quite readable, and Jetpack Compose's declarative approach removed a lot of the view setup boilerplate I remembered from years ago.

In under an hour I had a basic greeting card app built with a name customization feature:

[![](https://audreyfeldroy.github.io/arg-static/img/%202023-12-15%20at%2011.24.52.png)](https://audreyfeldroy.github.io/arg-static/img/%202023-12-15%20at%2011.24.52.png)

  

On the right side of Android Studio, the design preview allowed me to see my composable GreetingPreview() rendered in realtime. GreetingPreview() is the function at the bottom which is annotated with @Preview and @Composable. That function is called a composable. Composables are the basic building blocks of UI in Jetpack Compose. A composable preview can be viewed in an Android Studio design pane without having to run the whole heavyweight emulator.

I'm happy with how simple yet powerful modern Android development has become. Compose in particular feels like the best way forward, leveraging Kotlin's strengths for declarative and reactive UIs. It has definitely rekindled my interest in building Android apps going forward.