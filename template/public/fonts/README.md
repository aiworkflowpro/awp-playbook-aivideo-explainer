# Fonts

Put the film's font files here (`.woff2`, `.woff`, `.ttf` or `.otf`) and list them in
`src/shared/fonts.ts`. They are loaded by the renderer before the first frame, so every segment,
every still and every render uses the same type. Do not rely on system fonts: they differ between
machines.

Use fonts whose license allows video and embedding, for example fonts under the SIL Open Font
License. Keep the license file next to the font.
