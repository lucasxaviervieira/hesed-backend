import cloudinary.uploader
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import db, Post

post_bp = Blueprint('posts', __name__, url_prefix='/posts')

@post_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    
    if not all(k in data for k in ("title", "author", "rich_text", "post_type")):
        return jsonify({'error': 'Campos obrigatórios ausentes'}), 400

    post = Post(
        title=data['title'],
        author=data['author'],
        rich_text=data['rich_text'],
        banner_img_src=data.get('banner_img_src', ''),
        post_type=data['post_type']
    )

    db.session.add(post)
    db.session.commit()
    
    return jsonify({'message': 'Post criado com sucesso', 'post_id': post.id}), 201


@post_bp.route('/upload-image', methods=['POST'])
@jwt_required()
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'Nenhuma imagem enviada'}), 400

    image = request.files['image']

    try:
        upload_result = cloudinary.uploader.upload(image)
        image_url = upload_result['secure_url']

        return jsonify({'message': 'Imagem enviada com sucesso!', 'image_url': image_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@post_bp.route('/', methods=['GET'])
def get_all_posts():
    posts = Post.query.all()
    return jsonify([
        {
            'id': p.id,
            'title': p.title,
            'author': p.author,
            'rich_text': p.rich_text,
            'banner_img_src': p.banner_img_src,
            'post_type': p.post_type,
            'created_at': p.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for p in posts
    ])


@post_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post não encontrado'}), 404

    return jsonify({
        'id': post.id,
        'title': post.title,
        'author': post.author,
        'rich_text': post.rich_text,
        'banner_img_src': post.banner_img_src,
        'post_type': post.post_type,
        'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S')
    })


@post_bp.route('/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post não encontrado'}), 404

    data = request.get_json()
    
    post.title = data.get('title', post.title)
    post.author = data.get('author', post.author)
    post.rich_text = data.get('rich_text', post.rich_text)
    post.banner_img_src = data.get('banner_img_src', post.banner_img_src)
    post.post_type = data.get('post_type', post.post_type)

    db.session.commit()

    return jsonify({'message': 'Post atualizado com sucesso'})


@post_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post não encontrado'}), 404

    db.session.delete(post)
    db.session.commit()

    return jsonify({'message': 'Post deletado com sucesso'})
