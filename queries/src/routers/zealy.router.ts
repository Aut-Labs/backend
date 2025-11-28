import { injectable } from "inversify";
import { Router } from "express";
import { ZealyController } from "../controllers/zealy.controller";
import { container } from "../inversify.config";
import { getNetworkConfig, LoggerService } from "../services";
import { NetworkConfigEnv } from "../models/config";

@injectable()
export class ZealyRouter {
  private readonly _router: Router;
  private readonly _zealyProdController: ZealyController;
  private readonly _zealyDevController: ZealyController;

  constructor() {
    this._router = Router({ strict: true });
    this._zealyDevController = new ZealyController(
      process.env.GRAPH_API_DEV_URL,
      getNetworkConfig(NetworkConfigEnv.Testnet),
      container.get<LoggerService>(LoggerService)
    );
    this._zealyProdController = new ZealyController(
      process.env.GRAPH_API_PROD_URL,
      getNetworkConfig(NetworkConfigEnv.Mainnet),
      container.get<LoggerService>(LoggerService)
    );
    this.init();
  }

  private validateApiKey(req, res, next) {
    const apiKey = req.header("X-Api-Key");
    if (!apiKey || apiKey !== process.env.ZEELY_API_KEY) {
      return res.status(401).send("Unauthorized");
    }
    next();
  }

  private init(): void {
    this._router.post(
      "/hasDeployed",
      this.validateApiKey,
      this._zealyProdController.hasDeployed
    );
    this._router.post(
      "/isAdmin",
      this.validateApiKey,
      this._zealyProdController.isAdmin
    );
    this._router.post(
      "/20members",
      this.validateApiKey,
      this._zealyProdController.has20Members
    );
    this._router.post(
      "/50members",
      this.validateApiKey,
      this._zealyProdController.has50Members
    );
    this._router.post(
      "/100members",
      this.validateApiKey,
      this._zealyProdController.has100Members
    );
    this._router.post(
      "/archetype",
      this.validateApiKey,
      this._zealyProdController.hasAddedAnArchetype
    );
    this._router.post(
      "/domain",
      this.validateApiKey,
      this._zealyProdController.hasRegisteredADomain
    );

    //DEV controller

    this._router.post(
      "/dev/hasDeployed",
      this.validateApiKey,
      this._zealyDevController.hasDeployed
    );
    this._router.post(
      "/dev/isAdmin",
      this.validateApiKey,
      this._zealyDevController.isAdmin
    );
    this._router.post(
      "/dev/20members",
      this.validateApiKey,
      this._zealyDevController.has20Members
    );
    this._router.post(
      "/dev/50members",
      this.validateApiKey,
      this._zealyDevController.has50Members
    );
    this._router.post(
      "/dev/100members",
      this.validateApiKey,
      this._zealyDevController.has100Members
    );
    this._router.post(
      "/dev/archetype",
      this.validateApiKey,
      this._zealyDevController.hasAddedAnArchetype
    );

    this._router.post(
      "/dev/domain",
      this.validateApiKey,
      this._zealyDevController.hasRegisteredADomain
    );
  }

  public get router(): Router {
    return this._router;
  }
}
