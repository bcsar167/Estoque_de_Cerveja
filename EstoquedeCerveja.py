
# Simulando um banco de dados com um dicionário
estoque = {}

@app.route('/cervejas', methods=['POST'])
def adicionar_cerveja():
    data = request.get_json()
    cerveja_id = data['id']
    estoque[cerveja_id] = data
    return jsonify({'message': 'Cerveja adicionada com sucesso!'}), 201

@app.route('/cervejas/<int:cerveja_id>', methods=['GET'])
def obter_cerveja(cerveja_id):
    cerveja = estoque.get(cerveja_id)
    if cerveja:
        return jsonify(cerveja)
    return jsonify({'message': 'Cerveja não encontrada!'}), 404

@app.route('/cervejas/<int:cerveja_id>', methods=['PUT'])
def atualizar_cerveja(cerveja_id):
    data = request.get_json()
    if cerveja_id in estoque:
        estoque[cerveja_id].update(data)
        return jsonify({'message': 'Cerveja atualizada com sucesso!'})
    return jsonify({'message': 'Cerveja não encontrada!'}), 404

@app.route('/cervejas/<int:cerveja_id>', methods=['DELETE'])
def deletar_cerveja(cerveja_id):
    if cerveja_id in estoque:
        del estoque[cerveja_id]
        return jsonify({'message': 'Cerveja deletada com sucesso!'})
    return jsonify({'message': 'Cerveja não encontrada!'}), 404

if __name__ == '__main__':
    app.run(debug=True)



    # test_app.py
    import pytest
    from app import app


    @pytest.fixture
    def client():
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client


    def test_adicionar_cerveja(client):
        response = client.post('/cervejas', json={'id': 1, 'nome': 'IPA', 'quantidade': 10})
        assert response.status_code == 201
        assert response.json == {'message': 'Cerveja adicionada com sucesso!'}


    def test_obter_cerveja(client):
        client.post('/cervejas', json={'id': 1, 'nome': 'IPA', 'quantidade': 10})
        response = client.get('/cervejas/1')
        assert response.status_code == 200
        assert response.json == {'id': 1, 'nome': 'IPA', 'quantidade': 10}


    def test_obter_cerveja_nao_existente(client):
        response = client.get('/cervejas/99')
        assert response.status_code == 404
        assert response.json == {'message': 'Cerveja não encontrada!'}


    def test_atualizar_cerveja(client):
        client.post('/cervejas', json={'id': 1, 'nome': 'IPA', 'quantidade': 10})
        response = client.put('/cervejas/1', json={'nome': 'IPA Premium', 'quantidade': 15})
        assert response.status_code == 200
        assert response.json == {'message': 'Cerveja atualizada com sucesso!'}


    def test_deletar_cerveja(client):
        client.post('/cervejas', json={'id': 1, 'nome': 'IPA', 'quantidade': 10})
        response = client.delete('/cervejas/1')
        assert response.status_code == 200
        assert response.json == {'message': 'Cerveja deletada com sucesso!'}


    def test_deletar_cerveja_nao_existente(client):
        response = client.delete('/cervejas/99')
        assert response.status_code == 404
        assert response.json == {'message': 'Cerveja não encontrada!'}





