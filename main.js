// main.js
const { app, BrowserWindow, Menu } = require('electron');
const path = require('path');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1400,
        height: 900,
        minWidth: 800,
        minHeight: 600,
        backgroundColor: '#1e3c72',
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        },
        icon: path.join(__dirname, 'assets/icon.png')
    });

    mainWindow.loadFile('index.html');

    // Menu personalizado
    const menu = Menu.buildFromTemplate([
        {
            label: 'Arquivo',
            submenu: [
                {
                    label: 'Exportar Relatório',
                    accelerator: 'CmdOrCtrl+E',
                    click: () => {
                        mainWindow.webContents.executeJavaScript('exportReport()');
                    }
                },
                { type: 'separator' },
                {
                    label: 'Sair',
                    accelerator: 'CmdOrCtrl+Q',
                    click: () => {
                        app.quit();
                    }
                }
            ]
        },
        {
            label: 'Ativos',
            submenu: [
                {
                    label: 'Adicionar Ativo',
                    accelerator: 'CmdOrCtrl+N',
                    click: () => {
                        mainWindow.webContents.executeJavaScript('document.getElementById("stock-symbol").focus()');
                    }
                },
                {
                    label: 'Atualizar Preços',
                    accelerator: 'F5',
                    click: () => {
                        mainWindow.webContents.executeJavaScript('updateStockPrices()');
                    }
                }
            ]
        },
        {
            label: 'Ferramentas',
            submenu: [
                {
                    label: 'DevTools',
                    accelerator: 'F12',
                    click: () => {
                        mainWindow.webContents.openDevTools();
                    }
                },
                { type: 'separator' },
                {
                    label: 'Recarregar',
                    accelerator: 'CmdOrCtrl+R',
                    click: () => {
                        mainWindow.reload();
                    }
                }
            ]
        },
        {
            label: 'Ajuda',
            submenu: [
                {
                    label: 'Documentação',
                    click: () => {
                        require('electron').shell.openExternal('https://github.com/seu-projeto');
                    }
                },
                { type: 'separator' },
                {
                    label: 'Sobre',
                    click: () => {
                        const { dialog } = require('electron');
                        dialog.showMessageBox(mainWindow, {
                            type: 'info',
                            title: 'Sobre',
                            message: 'Sistema de Análise de Investimentos',
                            detail: 'Versão 1.0.0\n\nEquipe:\n- Mateus Lima\n- Matheus Araújo\n- Udiel\n- Kauã Fernandes\n\nOrientador: Prof. Vander',
                            buttons: ['OK']
                        });
                    }
                }
            ]
        }
    ]);

    Menu.setApplicationMenu(menu);

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (mainWindow === null) {
        createWindow();
    }
});
