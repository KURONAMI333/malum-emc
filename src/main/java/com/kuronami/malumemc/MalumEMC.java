package com.kuronami.malumemc;

import com.mojang.logging.LogUtils;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import org.slf4j.Logger;

/**
 * Malum ProjectE EMC — data-only integration. EMC values + transcribed Malum
 * recipes live in {@code data/malum/pe_custom_conversions/} (loaded by ProjectE
 * via datapack reload); this class only provides the {@code @Mod} entry point.
 */
@Mod(MalumEMC.MODID)
public final class MalumEMC {
    public static final String MODID = "malum_emc";
    public static final String VERSION = "0.1.0";
    private static final Logger LOGGER = LogUtils.getLogger();

    public MalumEMC(IEventBus modBus) {
        LOGGER.info("Malum ProjectE EMC v{} loading — EMC via data/malum/pe_custom_conversions", VERSION);
    }
}
