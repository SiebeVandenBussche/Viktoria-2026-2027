# VEX V5 Robot — `develop` branch

---

## Nederlands

### Overzicht

Dit is de **`develop` branch** van het VEX V5 robotproject. Deze branch dient als integratiebranch voor alle nieuwe functies en verbeteringen die klaarstaan voor de volgende release.

> De code in deze branch is **in actieve ontwikkeling** en mogelijk niet stabiel. Gebruik de `main`/`master` branch voor productie-klare code.

### Branch-structuur

Dit project volgt het **git-flow** branching model:

| Branch | Doel |
|---|---|
| `master` / `main` | Stabiele, productie-klare code |
| `develop` | Integratiebranch voor nieuwe ontwikkelingen |
| `feature/*` | Individuele functies, vertakt vanuit `develop` |
| `release/*` | Voorbereiding van een nieuwe release |
| `hotfix/*` | Urgente fixes op de productieversie |

### Werken met deze branch

**Nieuwe functie starten:**
```bash
git checkout develop
git checkout -b feature/mijn-functie
```

**Functie afronden en samenvoegen:**
```bash
git checkout develop
git merge --no-ff feature/mijn-functie
git branch -d feature/mijn-functie
git push origin develop
```

### Bijdragen

1. Maak altijd een `feature/*` branch aan vanuit `develop`
2. Duw **nooit** rechtstreeks naar `master`
3. Zorg dat je code getest is op de VEX V5 hardware voor je samenvoegt
4. Gebruik duidelijke commit-berichten

---

## English

### Overview

This is the **`develop` branch** of the VEX V5 robotics project. This branch serves as the integration branch for all new features and improvements that are ready for the next release.

> Code in this branch is **actively under development** and may not be stable. Use the `main`/`master` branch for production-ready code.

### Branch Structure

This project follows the **git-flow** branching model:

| Branch | Purpose |
|---|---|
| `master` / `main` | Stable, production-ready code |
| `develop` | Integration branch for new development |
| `feature/*` | Individual features, branched off from `develop` |
| `release/*` | Preparation of a new release |
| `hotfix/*` | Urgent fixes on the production version |

### Working with this branch

**Starting a new feature:**
```bash
git checkout develop
git checkout -b feature/my-feature
```

**Finishing and merging a feature:**
```bash
git checkout develop
git merge --no-ff feature/my-feature
git branch -d feature/my-feature
git push origin develop
```

### Contributing

1. Always create a `feature/*` branch from `develop`
2. **Never** push directly to `master`
3. Make sure your code is tested on the VEX V5 hardware before merging
4. Use clear and descriptive commit messages
