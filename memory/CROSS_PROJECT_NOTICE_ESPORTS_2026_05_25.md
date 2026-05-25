# Cross-project notice — ESPORTS opportunity missed 2026-05-20

User flagged ESPORTS (BSC, Yooldo Games) as missed opportunity. Our data:
- feed_onchain.jsonl: **190 ESPORTS whale alerts** from @Капитанская_каюта
- Pattern: wallet 0x7ef9...10dd → fresh wallet 0x5e63...bc73, $1.81M+ accumulated in minutes
- Classic pre-pump whale-to-fresh transfer pattern
- 2026-05-20 18:42 UTC onwards

What happened:
- Funding-rate Claude: cannot trade DEX token (no CEX perp listing)
- OnChain Claude: **DID NOT mention ESPORTS in any cycle insight** (checked cycle_*.md)
- OnChain bot sniper_state: 0 ESPORTS trades

OnChain Claude — investigate why ESPORTS slipped through:
1. Was it in your feed_onchain.jsonl? YES (190 alerts).
2. Did your wallet-tagger fire? Likely NO (BSC wallet, your focus is Solana).
3. Is your "fresh wallet receiving large $" filter triggered? Should have — $1.81M to fresh wallet is well above threshold.
4. Why no H-hypothesis catches BSC pump pre-accumulation?

Action items for OnChain:
- Audit your fresh-wallet detector on BSC vs Solana
- Add BSC accumulation as separate hypothesis class (H_BSC_PRE_PUMP)
- Quantify what you missed: ESPORTS price action after 2026-05-20 18:42 UTC

Funding-rate side: catalogued as H_LISTING_BRIDGE candidate — IF ESPORTS gets CEX perp listing within 14 days of whale-accumulation alerts, that's a basis-arb opportunity (DEX spot vs CEX perp at listing). Need cross-project handoff for execution.

Filed by funding-rate Claude per user request 2026-05-25.
