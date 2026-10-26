# Apply this website update

This ZIP contains the changed website files, the bundled mathematics renderer, two extracted question figures, and your supplied 2021–22 term-test PDF. It is an update for the existing complete website. Keep your original assets.

1. Extract `semester-study-archive-update.zip` into a temporary folder.
2. In GitHub Desktop, select your website repository, then **Repository → Show in Explorer**.
3. Copy everything inside the extracted update folder into this cloned website folder, beside the existing `index.html`.
4. Choose **Replace the files in the destination** for matching filenames. Merge `assets`; retain all the existing PDFs, diagrams and question scans.
5. Ensure the new `vendor` folder is beside `index.html`. It contains the equation renderer and fonts.
6. In GitHub Desktop, enter `Simplify collections and format solutions` in Summary. Click **Commit to main**, then **Push origin**.
7. After GitHub Pages finishes deploying, refresh the website with **Ctrl+F5**.

Replace `index.html`, `app.js`, `style.css` and `data.json` together. Replacing only the index will not install the new reader.

## Three collections

- Session 2020–21: Machine Learning, Computer Security, Software Project Management and HCI finals.
- Session 2019–20: Machine Learning and Software Project Management finals.
- Batch 2021–22: the supplied 13-page term-test solution PDF with subject shortcuts.

The additional 2023 Security paper remains as supplementary material. Its session is not printed and is not relabeled as 2019–20. The previous SPM term exercise is retained under supporting material in the 2020–21 collection.

## Reading and PDFs

Questions appear before answers. The new reader uses blue headings, worked steps, tables, supporting figures, typeset mathematics and green answer summaries. The math renderer and fonts are included locally.

Use **Print / save answers as PDF** for the new layout. Clear the search field first to print a complete course. Older study PDFs are under **Original scans, revision notes & supporting files** and keep their previous layout.

Question headings may be restated for readability. Original papers remain the source for exact wording, instructions and marks. Existing study answers are retained and reformatted; this update is not a full independent academic review or official answer key.

## Editing later

Each `data.json` item has `question`, optional `questionBlocks`, `blocks` for the displayed answer, and `final` for its summary. Supported block types are `p`, `heading`, `list`, `table`, `math`, `code` and `image`. A math block contains `tex`; text blocks support inline LaTeX between `\( ... \)`.

The original `body` is retained for search. Edit the displayed `blocks` to change a visible answer. Legacy Python generators in `tools/` create the previous data format; adapt them before running them, or they will overwrite the new formatting.

This remains a static website suitable for GitHub Pages, Netlify and Vercel. No build step is required. This update has not been pushed to your public repository automatically.
