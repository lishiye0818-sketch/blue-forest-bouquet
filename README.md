# Blue Forest · Streamlit Community Cloud

This repository runs the existing Blue Forest application directly on Streamlit,
including Customer, Staff, DIY selling prices and genuine CLIP/FAISS Top 2 search.

Deploy `main` → `streamlit_app.py`, with **Python 3.12**. Use the repository-root
`requirements.txt`; no Vercel project or Docker build is needed.

The repository contains the current 20 materials, their images, four shop
bouquets and Staff-edited unit prices/BOMs. On first launch, it initializes a
writable runtime database and images without replacing existing runtime edits.
The exact existing CLIP model is fetched from pinned public Hugging Face
revisions and SHA-256 checked, then reused locally. It is not a paid API.

The first cold launch can take several minutes. Test search on the actual cloud
instance to check available memory. All material images ship with the source.

Community Cloud does not guarantee local file persistence. Staff changes/uploads
can be lost when its filesystem is replaced. A persistent-volume deployment is
required for durable operation. The enquiry queue remains browser-session based;
Customer/Staff switching is a demonstration view, not account authentication.

Local historical quotation records are not published in this deployment seed.
They remain in the original local database and the earlier private backup package.
New sessions start with an empty enquiry queue. Original application logic,
selling-price formulas and quotation snapshot creation remain unchanged.

See `manifest.json` for image/index verification and catalog row counts.
