import { describe, expect, it } from "vitest";
import { buildGenerateOptionsFromConfig } from "./config-utils";
import { generateClashConfig } from "../generator";
import { isCustomRuleType } from "../rules/custom-rule-utils";

describe("portable NETWORK rules", () => {
  it("preserves UDP through saved config normalization and final generation", () => {
    const config = {customRules: [{id:"udp",type:"NETWORK",value:" UDP ",target:"REJECT"}]};
    const options = buildGenerateOptionsFromConfig(JSON.parse(JSON.stringify(config)), {nodes: []});
    expect(isCustomRuleType("NETWORK")).toBe(true);
    expect(generateClashConfig(options).rules).toContain("NETWORK,udp,REJECT");
  });
  it("rejects malformed protocol values rather than injecting another rule", () => {
    const options = buildGenerateOptionsFromConfig({customRules: [{id:"bad",type:"NETWORK",value:"udp,DIRECT",target:"REJECT"}]}, {nodes: []});
    expect(generateClashConfig(options).rules.some(r => r.startsWith("NETWORK,"))).toBe(false);
  });
});
