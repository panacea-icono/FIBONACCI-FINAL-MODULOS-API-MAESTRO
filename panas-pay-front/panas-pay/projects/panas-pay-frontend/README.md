# 🚀 PanasPay Frontend

> **Decentralized P2P payment platform on Algorand**
> Direct exchange between users without custody, prioritizing reputation and transparency

## 📋 Project Description

**PanasPay** is a decentralized application (dApp) built on the Algorand blockchain that enables:

- 💱 **P2P Exchanges**: Direct transactions between users without intermediaries
- 🔒 **Non-Custodial**: Users maintain full control of their funds
- ⭐ **Reputation System**: User evaluation for greater trust
- 🌐 **Native Web3**: Complete integration with Algorand wallets
- 🏥 **Medical Focus**: Optimized for medical services and products

## 🛠️ Technology Stack

### Frontend

- **React 18.3.1** - User interface library
- **TypeScript 5.1.6** - Static typing for greater robustness
- **Vite 5.4.19** - Modern and fast build tool
- **Tailwind CSS 3.3.2** - Utility-first CSS framework
- **daisyUI 4.0.0** - UI components for Tailwind

### Blockchain & Web3

- **Algorand** - Pure proof-of-stake blockchain
- **AlgoKit 2.8.0** - Official toolkit for Algorand development
- **use-wallet** - React hooks for wallet integration
- **AlgoSDK** - Official Algorand SDK

### Development Tools

- **ESLint** - JavaScript/TypeScript code linting
- **Prettier** - Automatic code formatting
- **Jest** - Testing framework
- **Playwright** - Browser testing
- **GitHub Actions** - Automated CI/CD

## 🚀 Quick Start

### Prerequisites

- **Node.js** ≥ 20.0
- **npm** ≥ 9.0
- **AlgoKit CLI** ≥ 2.0.0
- **Docker** (for LocalNet)

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd panas-pay
   ```

2. **Install workspace dependencies**

   ```bash
   algokit project bootstrap all
   ```

3. **Configure local environment**

   ```bash
   cd projects/panas-pay-frontend
   # The .env file is generated automatically
   ```

4. **Start Algorand local network**

   ```bash
   cd ../panas-pay-contracts
   algokit localnet start
   ```

5. **Compile smart contracts**

   ```bash
   npm run build
   ```

6. **Run frontend**

   ```bash
   cd ../panas-pay-frontend
   npm run dev
   ```

## 🔧 Development Commands

### Frontend Commands

```bash
npm run dev          # Development server
npm run build        # Production build
npm run test         # Run tests
npm run lint         # Code linting
npm run lint:fix     # Fix linting issues
```

### Smart Contracts

```bash
npm run build        # Compile contracts
npm run test         # Run tests
npm run deploy       # Deploy to local network
npm run audit        # Security audit
```

### Workspace (from root)

```bash
algokit project run build    # Build all projects
algokit project run test     # Test all projects
algokit project run lint     # Lint all projects
```

## 🌐 Network Configuration

### LocalNet (Development)

```env
VITE_ALGOD_NETWORK=localnet
VITE_ALGOD_SERVER=http://localhost
VITE_ALGOD_PORT=4001
VITE_ALGOD_TOKEN=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

### TestNet (Testing)

```env
VITE_ALGOD_NETWORK=testnet
VITE_ALGOD_SERVER=https://testnet-api.algonode.cloud
VITE_ALGOD_TOKEN=
```

### MainNet (Production)

```env
VITE_ALGOD_NETWORK=mainnet
VITE_ALGOD_SERVER=https://mainnet-api.algonode.cloud
VITE_ALGOD_TOKEN=
```

## 🔌 Wallet Integration

### Supported Wallets

- **LocalNet**: KMD (Key Management Daemon)
- **TestNet/MainNet**:
  - Pera Wallet
  - Defly Wallet
  - Exodus Wallet
  - Daffi Wallet

### Usage Example

```typescript
import { useWallet } from '@txnlab/use-wallet-react'

function WalletConnect() {
  const { activeAccount, signTransactions } = useWallet()

  // Connection logic
}
```

## 📁 Project Structure

```text
panas-pay-frontend/
├── src/
│   ├── components/          # React components
│   │   ├── ConnectWallet.tsx
│   │   ├── Transact.tsx
│   │   └── AppCalls.tsx
│   ├── contracts/           # Contract clients (generated)
│   ├── utils/               # Utilities and helpers
│   ├── interfaces/          # TypeScript types
│   └── styles/              # CSS styles
├── public/                  # Static files
├── tests/                   # Application tests
└── .github/                 # CI/CD workflows
```

## 🧪 Testing

### Unit Tests

```bash
npm run test                 # Jest with coverage
npm run test:watch          # Watch mode
```

### E2E Tests

```bash
npm run playwright:test     # Playwright tests
```

## 🚀 Deployment

### Vercel

1. Configure environment variables
2. Connect GitHub repository
3. Automatic deployment on push to main

### Netlify

1. Configure environment variables
2. Connect GitHub repository
3. Automatic deployment on push to main

## 🔒 Security

- **Environment Variables**: All sensitive keys in `.env` files
- **Audit**: `npm audit` to check for vulnerabilities
- **Linting**: ESLint to maintain code standards
- **TypeScript**: Strict typing to prevent runtime errors

## 🤝 How to Contribute

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the [MIT](LICENSE) license.

## 🆘 Support

- **Documentation**: [AlgoKit Docs](https://github.com/algorandfoundation/algokit-cli)
- **Algorand**: [Developer Portal](https://developer.algorand.org/)
- **Issues**: [GitHub Issues](https://github.com/your-org/panas-pay/issues)

## 📊 Project Status

- **Version**: 0.1.0
- **Status**: 🟡 In Development
- **Last Update**: 2024-08-31
- **Network**: 🟢 LocalNet | 🟡 TestNet | 🔴 MainNet

---

> **Developed with ❤️ by Panacea Icono S.A.**
> _Transforming healthcare through blockchain technology_
