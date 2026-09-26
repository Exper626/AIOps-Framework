// Pages shown in place of the chat. The chat behind them stays as it was, so
// opening one doesn't start a new chat.
export function isPageRoute(pathname: string) {
  return pathname.startsWith("/saved");
}
