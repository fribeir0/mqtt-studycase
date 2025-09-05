# Vulnerabilidades e Medidas de Correção - MQTT Broker

## Vulnerabilidades Encontradas

### 1. Falta de autenticação

O broker permitia conexões anônimas, possibilitando que qualquer cliente publicasse ou assinasse tópicos sem restrições.

### 2. Ausência de políticas de controle de acesso (ACL)

Não havia granularidade de permissões para definir quem poderia publicar ou assinar determinados tópicos.

### 3. Tráfego não criptografado

A comunicação cliente-servidor ocorria em texto puro, expondo credenciais e dados sensíveis a ataques de interceptação (Man-in-the-Middle).

---

## ✅ Medidas de Correção Implementadas

### 1. Autenticação de Usuários

- Configuração do `mosquitto.conf` para exigir autenticação.
- Criação de um arquivo de senhas com `mosquitto_passwd`.

### 2. Políticas de Controle de Acesso (ACL)

- Implementação de arquivo `acl_file` para definir granularidade de acesso (quem pode publicar e/ou ler tópicos específicos).

### 3. Criptografia de Tráfego com TLS

- Habilitação de criptografia na porta **8883**.
- Geração e configuração de certificados TLS (CA, servidor e clientes).

---

## 🚀 Resultado Final

- **Autenticação**: Agora, apenas usuários autenticados podem acessar o broker.
- **Controle de Acesso (ACL)**: Permissões detalhadas para publicação e leitura de tópicos.
- **Criptografia TLS**: Toda comunicação agora é criptografada, garantindo a segurança dos dados transmitidos.

- <img width="806" height="328" alt="image" src="https://github.com/user-attachments/assets/8884cb22-796f-4687-adbf-e8ddf0825c62" />


