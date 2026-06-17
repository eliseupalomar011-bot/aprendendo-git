# TrinityOS Next — Arquitetura

Base: OpenHarmony (Standard) + TrinityKernel 8.7

## Camadas
- Base OpenHarmony: serviços e framework do sistema
- Trinity Layer: UI, serviços Trinity e empacotamento `.otn`
- Compat: subsistemas (Android/Windows) como camadas, não base

## Diretórios
- trinity/ui: shell, control center, lockscreen, launcher
- trinity/services: core/power/security/update
- trinity/pkg: otn-spec/installer/tat
- trinity/compat: android-subsystem/windows-layer

## Princípios
- Modularidade: tudo removível/atualizável
- Segurança: pacotes assinados + sandbox
- Compatibilidade via subsistemas (não vira Android)
