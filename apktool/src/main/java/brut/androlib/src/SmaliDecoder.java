/**
 *  Copyright 2014 Ryszard Wiśniewski <brut.alll@gmail.com>
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

package brut.androlib.src;

import org.jf.baksmali.Baksmali;
import org.jf.baksmali.BaksmaliOptions;
import org.jf.dexlib2.DexFileFactory;
import org.jf.dexlib2.Opcodes;
import org.jf.dexlib2.analysis.InlineMethodResolver;
import org.jf.dexlib2.dexbacked.DexBackedDexFile;
import org.jf.dexlib2.dexbacked.DexBackedOdexFile;

import java.io.File;
import java.io.IOException;

import brut.androlib.AndrolibException;

/**
 * @author Ryszard Wiśniewski <brut.alll@gmail.com>
 */
public class SmaliDecoder {

    public static void decode(File apkFile, File outDir, String dexName, boolean bakdeb, int api)
            throws AndrolibException {
        new SmaliDecoder(apkFile, outDir, dexName, bakdeb, api).decode();
    }

    private SmaliDecoder(File apkFile, File outDir, String dexName, boolean bakdeb, int api) {
        mApkFile = apkFile;
        mOutDir  = outDir;
        mDexFile = dexName;
        mBakDeb  = bakdeb;
        mApi     = api;
    }

    private void decode() throws AndrolibException {
        try {
            BaksmaliOptions options = new BaksmaliOptions();

            // Get API opcodes
            Opcodes opcodes = Opcodes.forApi(mApi);

            // Load the dex file using correct API for baksmali 2.5.2
            DexBackedDexFile dexFile = DexFileFactory.loadDexFile(mApkFile, opcodes);

            if (dexFile instanceof DexBackedOdexFile) {
                options.inlineResolver =
                        InlineMethodResolver.createInlineMethodResolver(((DexBackedOdexFile)dexFile).getOdexVersion());
            }

            // Disassemble using correct API for baksmali 2.5.2
            Baksmali.disassembleDexFile(dexFile, mOutDir, options);

        } catch (IOException ex) {
            throw new AndrolibException(ex);
        }
    }

    private final File mApkFile;
    private final File mOutDir;
    private final String mDexFile;
    private final boolean mBakDeb;
    private final int mApi;
}
