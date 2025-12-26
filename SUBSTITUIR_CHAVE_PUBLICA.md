# Como Substituir a Chave Pública da Krux

Este guia explica como substituir a chave pública da Krux por uma chave própria para poder fazer atualizações pelo SD card.

## Passo 1: Gerar um Par de Chaves

Execute o script para gerar um novo par de chaves:

```bash
cd /home/fabricio/Downloads/krux
python scripts/generate_keys.py
```

Isso criará dois arquivos:
- `private.pem` - Sua chave privada (MANTENHA SEGURA E SECRETA!)
- `public.hex` - Sua chave pública (pode ser compartilhada)

O script também mostrará a chave pública em formato hexadecimal no terminal.

## Passo 2: Substituir a Chave Pública no Código

Edite o arquivo `src/krux/metadata.py` e substitua o valor de `SIGNER_PUBKEY`:

```python
SIGNER_PUBKEY = "SUA_CHAVE_PUBLICA_AQUI"
```

Onde `SUA_CHAVE_PUBLICA_AQUI` é a chave pública gerada no Passo 1 (formato hexadecimal, sem espaços).

**Exemplo:**
```python
VERSION = "25.10.1"
SIGNER_PUBKEY = "03abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"
```

## Passo 3: Compilar o Firmware

Após substituir a chave pública, você precisará recompilar o firmware para que a nova chave seja incluída:

```bash
# Siga o processo normal de build da Krux
# (consulte a documentação de build da Krux)
```

## Passo 4: Assinar Firmwares com Sua Chave Privada

Quando você criar um firmware para atualização via SD card, assine-o com sua chave privada:

```bash
python scripts/sign_firmware.py firmware.bin private.pem
```

Isso criará o arquivo `firmware.bin.sig` que é necessário para a verificação.

## Passo 5: Atualizar via SD Card

1. Coloque o `firmware.bin` e `firmware.bin.sig` na raiz do SD card
2. Insira o SD card no dispositivo
3. Inicie o dispositivo - a Krux detectará automaticamente o novo firmware
4. Se a assinatura corresponder à chave pública no firmware, a atualização será permitida

## Importante

⚠️ **SEGURANÇA:**
- **NUNCA** compartilhe sua chave privada (`private.pem`)
- Mantenha a chave privada em local seguro
- Faça backup da chave privada (se você perdê-la, não poderá mais assinar firmwares)
- A chave pública pode ser compartilhada livremente

⚠️ **COMPATIBILIDADE:**
- Firmwares assinados com a chave antiga da Krux NÃO funcionarão mais
- Você só poderá instalar firmwares assinados com sua nova chave privada
- Se você quiser voltar a usar firmwares oficiais da Krux, precisará reverter a mudança

## Verificar Assinatura

Para verificar se um firmware está corretamente assinado antes de colocá-lo no SD card:

```bash
python scripts/verify_firmware.py firmware.bin SUA_CHAVE_PUBLICA_HEX
```

Onde `SUA_CHAVE_PUBLICA_HEX` é sua chave pública em formato hexadecimal.

