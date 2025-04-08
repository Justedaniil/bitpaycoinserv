document.addEventListener("DOMContentLoaded", () => {
    // ✅ Vérification de l'existence du conteneur de features
    const featuresContainer = document.getElementById("features-container");

    if (!featuresContainer) {
        console.error("⚠️ ERREUR : Le conteneur 'features-container' est introuvable !");
    } else {
        const features = [
            { title: "Voir le Solde", subtitle: "Consultez votre balance actuelle", href: "/solde", icon: "/static/images/wallet-icon.png" },
            { title: "Historique", subtitle: "Suivez vos transactions", href: "/transactions", icon: "/static/images/transactions-icon.png" },
            { title: "Scanner QR", subtitle: "Scannez pour payer", href: "/scanner", icon: "/static/images/qr-icon.png" },
            { title: "Factures", subtitle: "Gérez vos factures", href: "/factures", icon: "/static/images/facture-icon.png" }
        ];

        // ✅ Génération des éléments pour chaque feature
        features.forEach(({ title, subtitle, href, icon }) => {
            const link = document.createElement("a");
            link.href = href;
            link.className = "feature-link";

            const img = document.createElement("img");
            img.src = icon;
            img.alt = title;
            img.className = "feature-icon";
            img.onerror = () => {
                console.error(`❌ Erreur de chargement pour l'icône de ${title}`);
                img.src = "/static/images/fallback-icon.png";
            };

            const textWrapper = document.createElement("div");
            textWrapper.className = "feature-text";

            const titleSpan = document.createElement("span");
            titleSpan.className = "feature-title";
            titleSpan.textContent = title;

            const subtitleSpan = document.createElement("span");
            subtitleSpan.className = "feature-subtitle";
            subtitleSpan.textContent = subtitle;

            textWrapper.append(titleSpan, subtitleSpan);
            link.append(img, textWrapper);
            featuresContainer.appendChild(link);
        });
    }

    
});
