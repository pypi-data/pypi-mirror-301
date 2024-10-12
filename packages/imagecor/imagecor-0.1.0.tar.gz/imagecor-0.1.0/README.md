# imagecor

imagecor est un package Python conçu pour traiter les images dans les fichiers Markdown. Il offre des fonctionnalités telles que le téléchargement d'images à partir d'URL, la conversion en noir et blanc, et le redimensionnement.

## Fonctionnalités

- Téléchargement d'images à partir d'URL dans les fichiers Markdown
- Conversion d'images en noir et blanc
- Redimensionnement d'images
- Mise à jour des liens d'images dans les fichiers Markdown
- Traitement par lots de fichiers Markdown

## Installation

Pour installer imagecor, vous pouvez utiliser pip :

```bash
pip install imagecor
```

Ou si vous utilisez Poetry :

```bash
poetry add imagecor
```

## Utilisation

Voici quelques exemples d'utilisation d'imagecor :

### Traitement d'un fichier Markdown

```python
from imagecor.image_processor import process_markdown_file

# Traiter un fichier Markdown, télécharger les images, convertir en noir et blanc et redimensionner
process_markdown_file('input.md', 'output_directory', convert_bw=True, max_size=(800, 600))
```

### Traitement du contenu Markdown

```python
from imagecor.image_processor import process_images

markdown_content = """
# Mon document

Voici une image : ![Une image](https://example.com/image.jpg)
"""

processed_content = process_images(markdown_content, 'output_directory', convert_bw=True, max_size=(800, 600))
```

## API

### `process_markdown_file(input_file, output_dir, convert_bw=False, max_size=None)`

Traite un fichier Markdown, télécharge les images, les traite optionnellement, et met à jour les liens dans le fichier.

- `input_file` : Chemin du fichier Markdown d'entrée
- `output_dir` : Répertoire de sortie pour le fichier Markdown traité et les images téléchargées
- `convert_bw` : Si True, convertit les images en noir et blanc
- `max_size` : Tuple (largeur, hauteur) pour le redimensionnement des images

### `process_images(content, output_dir, convert_bw=False, max_size=None)`

Traite le contenu Markdown, télécharge les images, les traite optionnellement, et met à jour les liens.

- `content` : Contenu Markdown à traiter
- `output_dir` : Répertoire de sortie pour les images téléchargées
- `convert_bw` : Si True, convertit les images en noir et blanc
- `max_size` : Tuple (largeur, hauteur) pour le redimensionnement des images



## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
