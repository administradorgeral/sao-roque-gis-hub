# Módulos do São Roque GIS Hub

## Arquitetura Modular

A aplicação foi reorganizada para seguir princípios de **desacoplamento** e **centralização apropriada**:

### 1. Opacity Manager (`opacity-manager.js`)
- **Objetivo**: Centralizar toda a programação de opacidade
- **Funcionalidades**:
  - Gerenciamento centralizado de todos os controles de opacidade
  - Registro de sliders para camadas
  - Aplicação consistente de opacidade em todas as camadas
  - Métodos para ajustar opacidade global ou individual

### 2. Layer Registry (`layer-registry.js`)
- **Objetivo**: Permitir carregamento dinâmico de camadas
- **Funcionalidades**:
  - Carregar camadas a partir de configurações
  - Configurar automaticamente toggles, sliders e botões
  - Registro e remoção dinâmica de camadas
  - Suporte a IDs flexíveis (com ou sem underscores, hífens, etc.)

### 3. Layer Manager (`layer-manager.js`)
- **Objetivo**: Gerenciar o ciclo de vida das camadas
- **Melhorias**:
  - Melhor suporte a opacidade em camadas GeoJSON
  - Notificações de eventos (registered, loaded, visibilityChanged, opacityChanged)

## Como Adicionar Novas Camadas

1. **Criar arquivo de configuração na pasta `js/layers/`**:
   ```javascript
   export const minhaCamadaConfig = {
     id: "minha-camada",
     name: "Nome da Camada",
     url: "data/minha-camada.geojson",
     defaultVisible: true,
     defaultOpacity: 0.6,
     cor: "#ff0000"
   };
   export default minhaCamadaConfig;
   ```

2. **Adicionar ao índice** (`js/layers/index.js`):
   ```javascript
   export { default as minhaCamadaConfig } from './minha-camada.js';
   export const ALL_LAYERS = [
     ...existingLayers,
     minhaCamadaConfig
   ];
   ```

3. **Adicionar elementos HTML** (opcional - o LayerRegistry tenta resolver IDs automaticamente):
   ```html
   <!-- Toggle -->
   <input type="checkbox" id="toggle-minha-camada">
   
   <!-- Slider de Opacidade -->
   <input type="range" id="opacity-minha-camada" min="0.1" max="1" step="0.05" value="0.6">
   
   <!-- Botão de Enquadramento -->
   <button id="btn-zoom-minha-camada">Enquadrar</button>
   ```

## Benefícios

1. **Desacoplamento**: Camadas podem ser adicionadas/removidas sem modificar o código principal
2. **Centralização de Opacidade**: Todas as configurações de opacidade em um só lugar
3. **Manutenção**: Fácil de adicionar, remover ou modificar camadas
4. **Flexibilidade**: IDs de elementos HTML são resolvidos automaticamente

## Observações

- O sistema tenta resolver IDs de elementos de forma inteligente
- Se os IDs não forem encontrados, um aviso é exibido no console
- A opacidade é aplicada de forma consistente a todas as camadas GeoJSON
