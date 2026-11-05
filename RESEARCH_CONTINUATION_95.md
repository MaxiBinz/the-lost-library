# E95: access check; no new finding

**3 November 2026.** E94 added a source-linked, provisional St Olaf reading and contextual comparison, so the preceding turn was progress. This pass did not obtain new manuscript evidence or change a historical conclusion.

## What happened

The accessible extracted text of Ville Walta's [2013 chapter](https://www.diva-portal.org/smash/get/diva2%3A668618/FULLTEXT01.pdf), pp. 20–21 and note 35, again describes a wider group of several manuscripts including IV.156, IV.157 and IV.173; it does not make them one book. That point was already recorded in [E28](RESEARCH_CONTINUATION_28.md). Selected parts were read, not the complete chapter. The separate 2025 [Vuori and Räsänen chapter](https://oa.finlit.fi/fi/books/184/files/5199443d-0be7-4f42-aaa1-425922b42d19.pdf) and the caption for its reproduction of IV.156 f.21r were already recorded in [E59](RESEARCH_CONTINUATION_59.md); f.21r is not the needed f.9 opening.

The following access attempts are logged so they are not repeated:

- **Publisher PDF via command-line HTTP:** one request to the exact 2025 publisher URL failed at DNS resolution, exit 6, before a response body; no PDF was saved. The in-app browser followed the ordinary publisher redirect but displayed a blank PDF surface. Browser transfer volume was not measured.
- **Web PDF screenshot:** screenshot calls for PDF page indexes 206, 207 and 208 all returned that screenshot support could not resolve the PDF content type. No page was displayed. E59 had already logged a failed screenshot of this PDF; attempting the screenshot route again was an error against the goal's no-retry rule. Stop using that route.
- **Walta PDF:** E28 had logged a full-PDF open timeout. This pass inadvertently opened/searched the same exact PDF URL through the web reader; extracted passages were returned, but the earlier failed-route restriction should have been checked first. Stop repeating that route. Previously visible indexed and newly returned text are not the unread Keskiaho 2008 or 2019 articles, and no full-chapter reading is claimed.

The resource audit before the HTTP attempt reported 209 working source-image files and a conservative planning total of 1,676,174,588 bytes including the historical reserve. The failed command saved zero bytes; web and browser transfer volumes are unmeasured. No manuscript image was obtained, and no contact, upload, external modification or publication took place.

A bounded search for the four exact phrase combinations `"IV.156" "9r" Olavi fragment`, `"IV.156" "fol. 9" "olavi"`, `"antifonarium" "IV.156" "Egregius"`, and `"F.m.IV.156" "9r" "olavi"` returned no identified reproduction of the relevant f.9 image. This is a search result for those queries, not proof that a reproduction does not exist.

## Consequence

This turn is classified **no progress** on the historical claim: the texts confirm existing project knowledge and the image test was not performed. Neither unsuccessful access nor this audit is evidence against a proposed historical relationship. The scientific question still requires a clearly identified original IV.156 or IV.157 comparator at the relevant text and signature, plus the Swedish side map. Pursue another meaningful already-authorized research test only after checking earlier failure logs and the complete source history; do not repeat failed URLs or use repeated generic comparisons as a substitute for discriminating evidence. The goal remains active.
